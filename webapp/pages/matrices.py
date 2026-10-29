import numpy as np
from nicegui import ui
from sympy import Float, Matrix, latex, nsimplify

from src.calculator import linear_algebra as la
from src.calculator import matrix as mx
from webapp import state
from webapp.layout import frame
from webapp.widgets import error_box, math, section

TWO_MATRIX = ['Addition', 'Subtraction', 'Multiplication']
ONE_MATRIX = ['Transpose', 'Determinant', 'Inverse', 'Rank', 'Eigenvalues', 'Scalar Multiplication']
NO_MATRIX = ['Identity Matrix', 'Zero Matrix']

ANALYSIS = [
    'Rank', 'Trace', 'Determinant', 'Inverse', 'Norm', 'Condition Number',
    'LU Decomposition', 'QR Decomposition', 'SVD', 'Eigenvalues', 'Eigenvectors',
    'Symmetric?', 'Orthogonal?', 'Positive Definite?',
]


def tidy(value):
    """
    Show near-integers as integers and values like 2.5 or 3.618... as
    1/2-style fractions or surds when that is exact; otherwise round.
    """

    value = float(np.real_if_close(value))

    if abs(value - round(value)) < 1e-10:
        return nsimplify(round(value))

    simple = nsimplify(value, tolerance=1e-12)
    if len(str(simple)) <= 20 and abs(float(simple) - value) < 1e-9 * max(1, abs(value)):
        return simple

    return Float(round(value, 6))


def matrix_latex(value):

    array = np.atleast_2d(np.asarray(value))

    if np.iscomplexobj(array) and not np.allclose(array.imag, 0):
        return latex(Matrix(array.tolist()).evalf(6), mat_delim='')

    return latex(Matrix([[tidy(v) for v in row] for row in np.real(array)]), mat_delim='')


def number_latex(value):

    if isinstance(value, (bool, np.bool_)):
        return r'\text{Yes}' if value else r'\text{No}'

    return latex(tidy(value))


def matrix_input(label, value):

    return ui.textarea(label, value=value) \
        .props('outlined autogrow input-class="font-mono"').classes('w-full')


@ui.page('/matrices')
def matrices_page():

    with frame('/matrices', 'Matrices', 'Write one row per line, numbers separated by spaces', 'grid_on'):

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            operation = ui.select(TWO_MATRIX + ONE_MATRIX + NO_MATRIX, value='Multiplication', label='Operation') \
                .props('outlined').classes('w-72')

            with ui.row().classes('w-full gap-4 no-wrap'):
                first = matrix_input('Matrix A', '1 2\n3 4')
                second = matrix_input('Matrix B', '5 6\n7 8')

            with ui.row().classes('gap-4'):
                scalar = ui.number('Scalar', value=2).props('outlined').classes('w-32')
                size = ui.number('Size', value=3, min=1, max=10, precision=0).props('outlined').classes('w-32')
                rows = ui.number('Rows', value=2, min=1, max=10, precision=0).props('outlined').classes('w-32')
                cols = ui.number('Columns', value=3, min=1, max=10, precision=0).props('outlined').classes('w-32')

            def update_inputs():
                op = operation.value
                first.visible = op not in NO_MATRIX
                second.visible = op in TWO_MATRIX
                scalar.visible = op == 'Scalar Multiplication'
                size.visible = op == 'Identity Matrix'
                rows.visible = cols.visible = op == 'Zero Matrix'

            operation.on_value_change(update_inputs)
            update_inputs()

            ui.button('Calculate', icon='calculate', on_click=lambda: calculate()).props('unelevated')

        output = ui.column().classes('w-full')

        def calculate():

            op = operation.value
            output.clear()

            try:
                a = mx.create_matrix(first.value) if op not in NO_MATRIX else None
                b = mx.create_matrix(second.value) if op in TWO_MATRIX else None

                if op == 'Addition':
                    question, result = rf'{matrix_latex(a)} + {matrix_latex(b)}', matrix_latex(mx.matrix_add(a, b))
                elif op == 'Subtraction':
                    question, result = rf'{matrix_latex(a)} - {matrix_latex(b)}', matrix_latex(mx.matrix_subtract(a, b))
                elif op == 'Multiplication':
                    question, result = rf'{matrix_latex(a)} {matrix_latex(b)}', matrix_latex(mx.matrix_multiply(a, b))
                elif op == 'Transpose':
                    question, result = rf'{matrix_latex(a)}^T', matrix_latex(mx.matrix_transpose(a))
                elif op == 'Determinant':
                    question, result = rf'\det {matrix_latex(a)}', number_latex(mx.matrix_determinant(a))
                elif op == 'Inverse':
                    question, result = rf'{matrix_latex(a)}^{{-1}}', matrix_latex(mx.matrix_inverse(a))
                elif op == 'Rank':
                    question, result = rf'\operatorname{{rank}} {matrix_latex(a)}', number_latex(mx.matrix_rank(a))
                elif op == 'Eigenvalues':
                    values, _ = mx.matrix_eigen(a)
                    question = rf'\lambda\left({matrix_latex(a)}\right)'
                    result = r',\quad '.join(rf'\lambda_{{{i}}} = {number_latex(v)}' if np.isreal(v)
                                            else rf'\lambda_{{{i}}} = {latex(complex(v))}'
                                            for i, v in enumerate(values, start=1))
                elif op == 'Scalar Multiplication':
                    question = rf'{number_latex(scalar.value)} \cdot {matrix_latex(a)}'
                    result = matrix_latex(mx.scalar_multiply(a, scalar.value))
                elif op == 'Identity Matrix':
                    question, result = rf'I_{{{int(size.value)}}}', matrix_latex(mx.identity_matrix(int(size.value)))
                else:
                    question = rf'0_{{{int(rows.value)} \times {int(cols.value)}}}'
                    result = matrix_latex(mx.zero_matrix(int(rows.value), int(cols.value)))

            except np.linalg.LinAlgError:
                with output:
                    error_box('This matrix has no inverse (its determinant is 0) or the sizes do not match.')
                return
            except Exception as error:
                with output:
                    error_box(error)
                return

            with output:
                with ui.card().classes('mm-card w-full shadow-none p-5'):
                    section(op)
                    math(f'{question} = {result}')

            state.add_history('Matrices', op, first.value, result)


@ui.page('/linear-algebra')
def linear_algebra_page():

    with frame('/linear-algebra', 'Linear Algebra', 'Rank, decompositions, eigenvalues and matrix checks', 'view_module'):

        with ui.card().classes('mm-card w-full shadow-none p-5 gap-3'):

            with ui.row().classes('w-full gap-4 no-wrap items-start'):
                matrix = matrix_input('Matrix', '4 1\n1 3').classes('max-w-md')
                operation = ui.select(ANALYSIS, value='Eigenvalues', label='Operation') \
                    .props('outlined').classes('w-72')

            ui.button('Compute', icon='calculate', on_click=lambda: compute()).props('unelevated')

        output = ui.column().classes('w-full')

        def compute():

            op = operation.value
            text = matrix.value
            output.clear()

            try:
                a = la.to_matrix(text)
                given = matrix_latex(a)

                if op == 'Rank':
                    parts = [('Rank', number_latex(la.matrix_rank(text)))]
                elif op == 'Trace':
                    parts = [('Trace', number_latex(la.matrix_trace(text)))]
                elif op == 'Determinant':
                    parts = [('Determinant', number_latex(la.matrix_determinant(text)))]
                elif op == 'Inverse':
                    parts = [('Inverse', matrix_latex(la.matrix_inverse(text)))]
                elif op == 'Norm':
                    parts = [('Norm', latex(round(float(la.matrix_norm(text)), 6)))]
                elif op == 'Condition Number':
                    parts = [('Condition', latex(round(float(la.matrix_condition(text)), 6)))]
                elif op == 'LU Decomposition':
                    p, l, u = la.lu_decomposition(text)
                    parts = [('P', matrix_latex(p)), ('L', matrix_latex(l)), ('U', matrix_latex(u))]
                elif op == 'QR Decomposition':
                    q, r = la.qr_decomposition(text)
                    parts = [('Q', matrix_latex(np.round(q, 4))), ('R', matrix_latex(np.round(r, 4)))]
                elif op == 'SVD':
                    u, s, vt = la.svd_decomposition(text)
                    parts = [('U', matrix_latex(np.round(u, 4))), (r'\Sigma', matrix_latex(np.diag(np.round(s, 4)))),
                             ('V^T', matrix_latex(np.round(vt, 4)))]
                elif op == 'Eigenvalues':
                    values = la.eigen_values(text)
                    parts = [(rf'\lambda_{{{i}}}', number_latex(v) if np.isreal(v) else latex(complex(np.round(v, 4))))
                             for i, v in enumerate(values, start=1)]
                elif op == 'Eigenvectors':
                    parts = [('V', matrix_latex(np.round(la.eigen_vectors(text), 4)))]
                elif op == 'Symmetric?':
                    parts = [(r'A = A^T', number_latex(la.symmetric(text)))]
                elif op == 'Orthogonal?':
                    parts = [(r'A^T A = I', number_latex(la.orthogonal(text)))]
                else:
                    parts = [('x^T A x > 0', number_latex(la.positive_definite(text)))]

            except np.linalg.LinAlgError:
                with output:
                    error_box('This operation is not possible for this matrix (for example, it is singular).')
                return
            except Exception as error:
                with output:
                    error_box(error)
                return

            with output:
                with ui.card().classes('mm-card w-full shadow-none p-5'):
                    section(op)
                    math(f'A = {given}')
                    for name, value in parts:
                        if '=' in name or '>' in name:
                            math(rf'{name} \;?\quad {value}')
                        elif name.isalpha() and len(name) > 1:
                            math(rf'\text{{{name}}} = {value}')
                        else:
                            math(f'{name} = {value}')

            state.add_history('Linear Algebra', op, text, parts[0][1])
