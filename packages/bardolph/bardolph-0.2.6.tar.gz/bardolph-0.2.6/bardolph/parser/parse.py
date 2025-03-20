#!/usr/bin/env python

import argparse
import logging

from bardolph.controller.routine import Routine, RuntimeRoutine
from bardolph.controller.units import UnitMode
from bardolph.lib import injection
from bardolph.lib.injection import inject
from bardolph.lib.symbol_table import SymbolType
from bardolph.lib.time_pattern import TimePattern
from bardolph.parser.code_gen import CodeGen
from bardolph.parser.context import Context
from bardolph.parser.expr_parser import ExpressionParser
from bardolph.parser.io_parser import IoParser
from bardolph.parser.lex import Lex
from bardolph.parser.loop_parser import LoopParser
from bardolph.parser.matrix_parser import MatrixParser
from bardolph.parser.token import Token, TokenTypes
from bardolph.runtime import bardolph_fn, i_runtime, runtime_module
from bardolph.vm.loader import Loader
from bardolph.vm.vm_codes import (JumpCondition, OpCode, Operand, Operator,
                                  Register, SetOp)


class Parser:
    def __init__(self):
        self._lexer = None
        self._error_output = ''
        self._context = Context()
        self._current_token = Token(TokenTypes.UNKNOWN)
        self._op_code = OpCode.NOP
        self._code_gen = CodeGen()
        self._tokens = iter([])
        self._command_map = {
            TokenTypes.ASSIGN: self._assignment,
            TokenTypes.BREAK: self._break,
            TokenTypes.BREAKPOINT: self._breakpoint,
            TokenTypes.DEFINE: self._definition,
            TokenTypes.GET: self._get_color,
            TokenTypes.IF: self._if,
            TokenTypes.MARK: self._mark,
            TokenTypes.NAME: self._call_routine,
            TokenTypes.NULL: self._syntax_error,
            TokenTypes.OFF: self._power_off,
            TokenTypes.ON: self._power_on,
            TokenTypes.PAUSE: self._pause,
            TokenTypes.PRINT: self._print,
            TokenTypes.PRINTF: self._printf,
            TokenTypes.PRINTLN: self._println,
            TokenTypes.RETURN: self._return,
            TokenTypes.REGISTER: self._set_reg,
            TokenTypes.REPEAT: self._repeat,
            TokenTypes.SET: self._set,
            TokenTypes.STAGE: self._stage,
            TokenTypes.UNITS: self._set_units,
            TokenTypes.WAIT: self._wait,
            None: self._syntax_error
        }
        self._token_trace = False

    def parse(self, input_string) -> bool:
        self._context.clear()
        self._code_gen.clear()
        self._error_output = ''
        self._load_runtime()
        self._tokens = Lex(input_string).tokens()
        self.next_token()
        return self._script()

    def get_program(self):
        return self._code_gen.program

    def parse_file(self, file_name):
        logging.debug('"{}"'.format(file_name))
        try:
            srce = open(file_name, 'r')
            input_string = srce.read()
            srce.close()
            return self.parse(input_string)
        except FileNotFoundError:
            logging.error('Error: file {} not found.'.format(file_name))
        except OSError:
            logging.error('Error accessing file {}'.format(file_name))

    def get_errors(self) -> str:
        return self._error_output

    @property
    def current_token(self):
        return self._current_token

    @inject(i_runtime.Runtime)
    def _load_runtime(self, runtime):
        for name, fn in runtime.get_fns().items():
            routine = RuntimeRoutine(name, fn)
            routine.params = bardolph_fn.params(fn)
            self._context.add_routine(routine)

    def _script(self) -> bool:
        return self._body() and self._eof()

    def _body(self) -> bool:
        while not self._current_token.is_a(TokenTypes.EOF):
            if not self._command():
                return False
        return True

    def _eof(self) -> bool:
        if not self._current_token.is_a(TokenTypes.EOF):
            return self.trigger_error("Didn't get to end of file.")
        return True

    def _command(self):
        return self._command_map.get(
            self._current_token.token_type, self._syntax_error)()

    def _set_reg(self):
        reg = Register.from_string(str(self._current_token))
        if reg is None:
            return self.token_error('Expected register, got "{}"')
        if reg is Register.TIME:
            return self._time()
        if self._current_token.is_a(TokenTypes.DEFAULT):
            self._add_instruction(OpCode.DEFAULT)
            return self.next_token()

        self.next_token()
        if self._current_token.is_a(TokenTypes.LITERAL_STRING):
            return self._string_to_reg(reg)
        return self._rvalue(reg)

    def _string_to_reg(self, reg) -> bool:
        if reg != Register.NAME:
            return self.trigger_error('Quoted value not allowed here.')
        self._add_instruction(OpCode.MOVEQ, self._current_token.content, reg)
        return self.next_token()

    def _set(self):
        return self._action(OpCode.COLOR)

    def _stage(self):
        if self._context.in_matrix() or self._context.in_routine():
            return self._action(OpCode.COLOR)
        return self.trigger_error(
            'Use of "stage" is not allowed in this context.')

    def _power_on(self):
        self._add_instruction(OpCode.MOVEQ, True, Register.POWER)
        return self._action(OpCode.POWER)

    def _power_off(self) -> bool:
        self._add_instruction(OpCode.MOVEQ, False, Register.POWER)
        return self._action(OpCode.POWER)

    def _action(self, op_code) -> bool:
        action_token = self._current_token.token_type
        self._op_code = op_code
        if not (self._context.in_matrix() or action_token is TokenTypes.STAGE):
            self._add_instruction(OpCode.WAIT)

        self.next_token()
        if self._current_token.is_a(TokenTypes.ALL):
            return self._all_operand()
        if self._current_token.is_a(TokenTypes.DEFAULT):
            return self._default_operand()
        return self._operand_list(action_token)

    def _all_operand(self) -> bool:
        if self._context.in_matrix():
            return self.trigger_error(
                'Use of "all" is not allowed in this context.')
        self._add_instruction(OpCode.MOVEQ, Operand.ALL, Register.OPERAND)
        self._add_instruction(self._op_code)
        return self.next_token()

    def _default_operand(self) -> bool:
        self._add_instruction(OpCode.MOVEQ, Operand.DEFAULT, Register.OPERAND)
        self._add_instruction(self._op_code)
        return self.next_token()

    def _operand_list(self, action_token) -> bool:
        """
        For every operand in the list, issue the instruction in
        self._op_code.
        """
        if action_token is TokenTypes.STAGE:
            if not MatrixParser(self).operand_list():
                return False
            self._add_instruction(OpCode.COLOR)
            return True

        if not self._operand():
            return False
        self._add_instruction(self._op_code)

        while self._current_token.is_a(TokenTypes.AND):
            self.next_token()
            if not self._operand():
                return False
            self._add_instruction(self._op_code)
        return True

    def _operand(self) -> bool:
        """
        Process a group, location, or light with an optional set of
        zones or rows/columns.
        """
        if self._current_token.is_a(TokenTypes.GROUP):
            operand = Operand.GROUP
            self.next_token()
        elif self._current_token.is_a(TokenTypes.LOCATION):
            operand = Operand.LOCATION
            self.next_token()
        else:
            operand = Operand.LIGHT

        const_str = self._current_str()
        if len(const_str) > 0:
            self._add_instruction(OpCode.MOVEQ, const_str, Register.NAME)
            self.next_token()
        elif self._current_token.is_a(TokenTypes.NAME):
            if not self._var_operand():
                return False
        else:
            if self._context.in_matrix():
                return self.trigger_error(
                    'Use of "set" not allowed in this context. Try "stage".')
            return self.token_error(
                'Needed a device, location, or group, got "{}".')

        if self._current_token.is_a(TokenTypes.ZONE):
            if not self._zone_range():
                return False
            operand = Operand.MZ_LIGHT
        elif self._current_token.is_any(
                TokenTypes.BEGIN, TokenTypes.COLUMN, TokenTypes.ROW):
            if operand is not Operand.LIGHT:
                return self.token_error(
                    '"{} not allowed with groups or locations.')
            if not MatrixParser(self).matrix_spec():
                return False
            operand = Operand.MATRIX_LIGHT

        self._add_instruction(OpCode.MOVEQ, operand, Register.OPERAND)
        return True

    def _zone_range(self) -> bool:
        if self._op_code is not OpCode.COLOR:
            return self.trigger_error('Zones not supported for {}'.format(
                self._op_code.name.lower()))
        self.next_token()
        return self._set_zones()

    def _set_zones(self, only_one=False):
        if not self._at_rvalue(False):
            return self.token_error('Expected zone number, got "{}"')
        return self._range(Register.FIRST_ZONE, Register.LAST_ZONE, only_one)

    def _range(self, first, last, only_one=False):
        if not self._rvalue(first):
            return False
        if not only_one and self._at_rvalue(False):
            return self._rvalue(last)

        self._add_instruction(OpCode.MOVEQ, None, last)
        return True

    def _var_operand(self) -> bool:
        name = str(self._current_token)
        if not self._context.has_symbol_typed(
                name, SymbolType.MACRO, SymbolType.VAR):
            return self.token_error('Undefined: {}')
        self._add_instruction(OpCode.MOVE, name, Register.NAME)
        return self.next_token()

    def _set_units(self) -> bool:
        self.next_token()
        if self._current_token.token_type not in (
                TokenTypes.RAW, TokenTypes.RGB, TokenTypes.LOGICAL):
            return self.token_error('Invalid parameter "{}" for units.')
        mode = UnitMode[self._current_token.token_type.name]
        self._add_instruction(OpCode.MOVEQ, mode, Register.UNIT_MODE)
        return self.next_token()

    def _wait(self) -> bool:
        self._add_instruction(OpCode.WAIT)
        return self.next_token()

    def _get_color(self) -> bool:
        self.next_token()
        if not self._at_rvalue(False):
            return self.token_error('Needed light name, got {}')
        if not self._rvalue():
            return False
        self._add_instruction(OpCode.MOVE, Register.RESULT, Register.NAME)
        self._add_instruction(OpCode.GET_COLOR)
        return True

    def _matrix_get(self) -> bool:
        if not self._context.in_matrix():
            return self.token_error("Can't get {} in this context.")
        mat_parser = MatrixParser(self)
        if self.current_token.is_a(TokenTypes.ALL):
            return mat_parser.get_all()
        if not mat_parser.operand_list():
            return False
        self._add_instruction(OpCode.GET_COLOR)
        return True

    def _pause(self):
        self._add_instruction(OpCode.PAUSE)
        self.next_token()
        return True

    def _print(self) -> bool:
        return IoParser(self).print()

    def _printf(self) -> bool:
        return IoParser(self).printf()

    def _println(self) -> bool:
        return IoParser(self).println()

    def _time(self):
        self.next_token()
        if self._current_token.is_a(TokenTypes.AT):
            self.next_token()
            return self._process_time_patterns()
        return self._rvalue(Register.TIME)

    def _process_time_patterns(self):
        time_pattern = self._current_time_pattern()
        if time_pattern is None:
            return self._time_spec_error()
        self._add_instruction(
            OpCode.TIME_PATTERN, SetOp.INIT, time_pattern)
        self.next_token()

        while self._current_token.is_a(TokenTypes.OR):
            self.next_token()
            time_pattern = self._current_time_pattern()
            if time_pattern is None:
                return self._time_spec_error()
            self._add_instruction(
                OpCode.TIME_PATTERN, SetOp.UNION, time_pattern)
            self.next_token()

        return True

    def _assignment(self) -> bool:
        self.next_token()
        if not self._current_token.is_a(TokenTypes.NAME):
            return self.token_error('Expected name for assignment, got "{}"')
        dest_name = str(self._current_token)
        if self._context.has_symbol_typed(dest_name, SymbolType.MACRO):
            return self.token_error('Attempt to assign to constant "{}"')
        self.next_token()
        if not self._rvalue(dest_name):
            return False
        self._context.add_variable(dest_name)
        return True

    def _rvalue(
            self,
            dest=Register.RESULT,
            code_gen=None) -> bool:
        """
        Consume the current token as an rvalue, generating the code to evaluate
        it and to move the result into dest.
        """
        code_gen = code_gen or self._code_gen
        if self._current_token.content == '{':
            return self.next_token() and self._rvalue_curly(dest, code_gen)
        if self._current_token.content == '[':
            return self._rvalue_fn_call(dest, code_gen)
        move_inst = OpCode.MOVE
        uminus = self._current_token.content == '-'
        if uminus:
            self.next_token()
        value = self._current_constant()
        if value is None and uminus:
            return self.token_error(
                'Outside expressions, a minus is allowed only for numbers.')
        if value is not None:
            move_inst = OpCode.MOVEQ
            if uminus:
                value *= -1
        elif self._current_token.is_a(TokenTypes.NAME):
            name = str(self._current_token)
            if self._context.has_symbol_typed(name, SymbolType.VAR):
                value = name
            else:
                if self._context.has_symbol(name):
                    return self.token_error('Not a value: "{}"')
                return self.token_error('Unknown: "{}"')
        elif self._current_token.is_a(TokenTypes.REGISTER):
            value = self._current_reg()
        elif self._current_token.content == 'not':
            return self._rvalue_not(dest, code_gen)
        else:
            return self.token_error('Cannot use {} as a value.')

        if dest is OpCode.PUSH:
            code_gen.push(value)
        elif value is not dest:
            code_gen.add_instruction(move_inst, value, dest)

        return self.next_token()

    def _rvalue_curly(self, dest, code_gen):
        if not self._rvalue_expr(dest, code_gen):
            return False
        if self.current_token != '}':
            return self.token_error("Expected closing curly brace, got {}.")
        return self.next_token()

    def _rvalue_fn_call(self, dest, code_gen):
        if not self._call_routine():
            return False
        if dest is OpCode.PUSH:
            code_gen.push(Register.RESULT)
        elif dest is not Register.RESULT:
            code_gen.add_instruction(OpCode.MOVE, Register.RESULT, dest)
        return True

    def _rvalue_not(self, dest, code_gen):
        self.next_token()
        if not ExpressionParser(self).expression():
            return False
        code_gen.add_instruction(OpCode.OP, Operator.NOT)
        return True

    def _rvalue_expr(self, dest, code_gen):
        if not ExpressionParser(self).expression():
            return False
        code_gen.pop(dest)
        return True

    def _at_rvalue(self, include_reg=True) -> bool:
        token = self.current_token
        if str(token) in '{[':
            return True
        if token.token_type in (
                TokenTypes.LITERAL_STRING,
                TokenTypes.NUMBER):
            return True
        if token.token_type is TokenTypes.REGISTER:
            return include_reg
        if self._current_token.is_a(TokenTypes.NAME):
            return not self._context.has_routine(str(self.current_token))
        return False

    def _definition(self) -> bool:
        self.next_token()
        if not self._current_token.is_a(TokenTypes.NAME):
            return self.token_error('Expected name for definition, got: {}')

        name = str(self._current_token)
        self.next_token()
        if self._detect_routine_start():
            if not self._context.get_routine(name).undefined:
                return self.token_error('Already defined: "{}"')
            return self._routine_definition(name)
        return self._macro_definition(name)

    def _detect_routine_start(self) -> bool:
        """
        If a definition is followed by "with", "begin", a keyword corresponding
        to a command, or the name of an existing routine, it's defining a new
        routine and not a variable.
        """
        if self._context.has_routine(str(self._current_token)):
            return True
        if self._current_token.token_type.is_executable():
            return True
        return self._current_token.is_any(TokenTypes.BEGIN, TokenTypes.WITH)

    def _macro_definition(self, name):
        """
        Process a "define" where an alias for a value is being created. This
        symbol exists at compile time. This means a define cannot refer to a
        parameter in a routine. The symbol has global scope, even if it is
        defined inside a routine.
        """
        value = self._current_literal()
        if value is None:
            inner_macro = self._context.get_macro(str(self._current_token))
            if inner_macro is None:
                return self.token_error('Macro needs constant, got "{}"')
            value = inner_macro.value
        self._context.add_global(name, SymbolType.MACRO, value)
        self._add_instruction(OpCode.CONSTANT, name, value)
        return self.next_token()

    def _routine_definition(self, name):
        if self._context.in_routine():
            return self.trigger_error('Nested definition not allowed.')

        self._context.enter_routine()
        self._add_instruction(OpCode.ROUTINE, name)

        routine = Routine(name)
        self._context.add_routine(routine)
        if self._current_token.is_a(TokenTypes.WITH):
            self.next_token()
            if not self._param_decl(routine):
                return False
        result = self.command_seq()
        self._add_instruction(OpCode.END, name)
        self._context.exit_routine()
        return result

    def _param_decl(self, routine):
        """
        The parameter declarations for the routine are not included in the
        generated code. Declarations are used only at compile time.
        """
        name = str(self._current_token)
        routine.add_param(name)
        self._context.add_variable(name)
        self.next_token()
        while (self._current_token.is_a(TokenTypes.NAME) and not
                self._context.has_routine(str(self._current_token))):
            name = str(self._current_token)
            if routine.has_param(name):
                self.token_error('Duplicate parameter name: "{}"')
                return None
            routine.add_param(name)
            self._context.add_variable(name)
            self.next_token()
        return True

    def command_seq(self) -> bool:
        if not self._current_token.is_a(TokenTypes.BEGIN):
            return self._command()
        return self.compound_command()

    def compound_command(self) -> bool:
        self.next_token()
        while not self._current_token.is_a(TokenTypes.END):
            if self._current_token.is_a(TokenTypes.EOF):
                return self.trigger_error('End of file before "end".')
            if not self._command():
                return False
        return self.next_token()

    def _call_routine(self) -> bool:
        if str(self._current_token) == '[':
            self.next_token()
            bracketed = True
        else:
            bracketed = False
        routine = self._context.get_routine(str(self._current_token))
        if routine.undefined:
            return self.token_error('Unknown name: "{}"')

        self._add_instruction(OpCode.CTX)
        self.next_token()
        for param_name in routine.value.params:
            if self.current_token == ']':
                return self.trigger_error(
                    'Missing parameter {}'.format(param_name))
            if not self._rvalue():
                return False
            self._add_instruction(OpCode.PARAM, param_name, Register.RESULT)
        self._add_instruction(OpCode.JSR, routine.name)
        if bracketed:
            if str(self.current_token) != ']':
                return self.trigger_error(
                    'No closing bracket for function call.')
            self.next_token()
        self._add_instruction(OpCode.END_CTX)

        return True

    def _return(self) -> bool:
        """
        The return value is put into the RESULT register. If there is no rvalue
        after the "return" keyword, the routine is just exiting, so put None
        into the register.
        """
        self.next_token()
        if self._at_rvalue():
            if not self._rvalue(Register.RESULT):
                return False
        else:
            self._code_gen.add_instruction(OpCode.MOVEQ, None, Register.RESULT)
        self._code_gen.add_instruction(OpCode.RETURN)
        return True

    def _mark(self):
        # In this context, not inside an rvalue, a freestanding expression is
        # an error. A routine that returns a value is still called, but the
        # return value is thrown away.
        if str(self.current_token) == '{':
            return self.token_error(
                "A mathematical expression is not allowed here.")
        if str(self.current_token == '['):
            return self._call_routine()
        return self.token_error("Unexpected character {}")

    def _if(self) -> bool:
        self.next_token()
        if not self._rvalue():
            return False
        marker = self._code_gen.if_true_start()
        if not self.command_seq():
            return False
        if self.current_token.is_a(TokenTypes.ELSE):
            self._code_gen.if_else(marker)
            self.next_token()
            if not self.command_seq():
                return False
        self._code_gen.if_end(marker)
        return True

    def _repeat(self) -> bool:
        result = LoopParser(self).repeat(self._code_gen, self._context)
        return result

    def _break(self) -> bool:
        if not self._context.in_loop():
            return self.trigger_error('Encountered "break" not inside loop.')
        inst = self._code_gen.add_instruction(
            OpCode.JUMP, JumpCondition.ALWAYS, self._code_gen.current_offset)
        self._context.add_break(inst)
        return self.next_token()

    def _add_instruction(self, op_code, param0=None, param1=None):
        return self._code_gen.add_instruction(op_code, param0, param1)

    def _add_message(self, message):
        self._error_output += '{}\n'.format(message)

    def trigger_error(self, message):
        full_message = 'Line {}: {}'.format(
            self._current_token.line_number, message)
        self._add_message(full_message)
        return False

    def _current_literal(self):
        """
        Interpret the current token as a literal and return its value. If the
        current token doesn't contain a literal, return None.
        """
        value = None
        text = str(self._current_token)
        if self._current_token.is_a(TokenTypes.NUMBER):
            value = int(text) if Lex.is_int(text) else float(text)
        elif self._current_token.is_a(TokenTypes.LITERAL_STRING):
            value = str(self._current_token)
        elif self._current_token.is_a(TokenTypes.TIME_PATTERN):
            value = TimePattern.from_string(str(self._current_token))
            if value is None:
                self._time_spec_error()
        return value

    def _current_constant(self):
        """
        Interpret the current token as either a literal or macro and return
        its value, which is known at compile time. If the token is an undefined
        name, return None.
        """
        value = self._current_literal()
        if value is not None:
            return value
        if not self._current_token.is_a(TokenTypes.NAME):
            return None
        macro = self._context.get_macro(str(self._current_token))
        return None if macro.undefined else macro.value

    def _current_int(self):
        value = self._current_constant()
        if isinstance(value, int):
            return value
        return round(value) if isinstance(value, float) else None

    def _current_float(self):
        value = self._current_constant()
        if isinstance(value, float):
            return value
        return float(value) if isinstance(value, int) else None

    def _current_str(self) -> str:
        value = self._current_constant()
        return value if isinstance(value, str) else ''

    def _current_time_pattern(self) -> TimePattern:
        """
        Returns the current token as a time pattern. Only literals or macros.
        """
        if self._current_token.is_a(TokenTypes.TIME_PATTERN):
            return TimePattern.from_string(str(self._current_token))
        if self._current_token.is_a(TokenTypes.NAME):
            return self._context.get_macro(str(self._current_token)).value
        return TimePattern(None, None)

    def _current_reg(self):
        if not self._current_token.is_a(TokenTypes.REGISTER):
            return None
        return Register.from_string(str(self._current_token))

    def next_token(self):
        if self._current_token != TokenTypes.EOF:
            try:
                self._current_token = next(self._tokens)
            except StopIteration:
                self._current_token = Token(TokenTypes.EOF)
                return self.trigger_error('Unexpected end of source.')
        if self._token_trace:
            logging.info(
                'Next token: "{}" ({})'.format(
                    self._current_token, self._current_token.token_type))
        return True

    def _breakpoint(self):
        self._code_gen.add_instruction(OpCode.BREAKPOINT)

    def token_error(self, message_format):
        return self.trigger_error(
            message_format.format(str(self._current_token)))

    def _unimplementd(self):
        return self.token_error('Unimplemented at token "{}"')

    def _syntax_error(self):
        return self.token_error('Unexpected input "{}"')

    def _time_spec_error(self):
        return self.token_error('Invalid time specification: "{}"')


def dump_routines(routines):
    print('\n\nRoutines\n========')
    for routine_name, routine in routines.items():
        print(routine_name)
        print('Start address: ', routine.get_address())
        print('Return address:', routine.get_return(), '\n')


def _init_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file', help='name of the script file')
    arg_parser.add_argument(
        '-a', '--assembly', help='output assembly', action='store_true')
    arg_parser.add_argument(
        '-l', '--load', help="use Loader", action='store_true')
    arg_parser.add_argument(
        '-v', '--verbose', help='list routine offsets', action='store_true')
    return arg_parser.parse_args()


def main():
    args = _init_args()
    injection.configure()
    runtime_module.configure()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s(%(lineno)d) %(funcName)s(): %(message)s')
    parser = Parser()
    if not parser.parse_file(args.file):
        print("Error compiling: {}".format(parser.get_errors()))
    else:
        output_code = parser.get_program()
        if args.load:
            loader = Loader()
            loader.load(output_code)
            routines = loader.get_routines()
            output_code = loader.get_code()

        inst_num = 0
        for inst in output_code:
            if args.assembly:
                print(inst.as_list_text())
            else:
                print('{:5d} {}'.format(inst_num, inst))
            inst_num += 1
        if args.verbose and args.load:
            dump_routines(routines)


if __name__ == '__main__':
    main()
