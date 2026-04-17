import os
from src.utils.utils import format_currency, parse_number
from src.service.service import DebtService, UserService, PaymentService

# -------------------------
# UTILIDADES
# -------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def draw_box(title, options):
    width = 50
    height = max(8, len(options) + 4)

    print("\n" + "_" * width)
    print(f"| {title.center(width - 4)} |")
    print("|" + " " * (width - 2) + "|")

    for opt in options:
        print(f"| {opt.ljust(width - 4)} |")

    for _ in range(height - len(options) - 3):
        print("|" + " " * (width - 2) + "|")

    print("|" + "_" * (width - 2) + "|")


def draw_table(title, headers, rows):
    # calcular ancho dinámico por columna
    col_widths = []

    for i in range(len(headers)):
        max_len = len(headers[i])
        for row in rows:
            max_len = max(max_len, len(str(row[i])))
        col_widths.append(max_len + 2)

    width = sum(col_widths) + (3 * len(headers)) + 1

    print("\n" + "_" * width)
    print(f"| {title.center(width - 4)} |")
    print("|" + "-" * (width - 2) + "|")

    # headers
    header_line = "|"
    for i, h in enumerate(headers):
        header_line += " " + h.center(col_widths[i]) + " |"
    print(header_line)

    print("|" + "-" * (width - 2) + "|")

    # filas
    for row in rows:
        row_line = "|"
        for i, col in enumerate(row):
            row_line += " " + str(col).ljust(col_widths[i]) + " |"
        print(row_line)

    print("|" + "_" * (width - 2) + "|")


# -------------------------
# MENÚS
# -------------------------

def main_menu():
    draw_box(
        "GESPAGOS: (APP FINANCIERA)",
        [
            "1. Registrar usuario",
            "2. Login",
            "3. Salir"
        ]
    )


def user_menu(name:str, debts, total_dbts):
    data = f"{name.title()}, DEUDAS[{debts}], TOTAL[{format_currency(total_dbts)}]"
    draw_box(
        "GESPAGOS: MENÚ USUARIO",
        [   data,
            "1. Crear deuda",
            "2. Ver deudas",
            "3. Agregar pago",
            "4. Ver pagos",
            "5. Logout o salir"
        ]
    )


# -------------------------
# CLI PRINCIPAL
# -------------------------
def safe_int(prompt):
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("❌ Debe ser un número válido")


def safe_number(prompt):
    while True:
        value = input(prompt)
        try:
            return parse_number(value)
        except ValueError:
            print("❌ Monto inválido")


def safe_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ No puede estar vacío")


def run_cli(user_service, debt_service, payment_service):
    current_user = None

    while True:
        try:
            if not current_user:
                clear()
                main_menu()
                option = input(">> ").strip()

                if option == "1":
                    uuid = safe_int("UUID: ")
                    email = safe_text("Email: ")
                    name = safe_text("Nombre: ")
                    password = safe_text("Contraseña: ")

                    result = user_service.register_user(uuid, email, name, password)
                    print("Resultado:", result)
                    input("\nENTER para continuar...")

                elif option == "2":
                    email = safe_text("Email: ")
                    password = safe_text("Contraseña: ")

                    user = user_service.log_user(email, password)

                    if user:
                        current_user = user
                    else:
                        print("❌ Credenciales incorrectas")
                        input("\nENTER para continuar...")

                elif option == "3":
                    print("Saliendo...")
                    break

                else:
                    print("❌ Opción inválida")
                    input("\nENTER para continuar...")

            else:
                clear()

                user_id = current_user[0]
                user_name = current_user[3]

                total_debts = debt_service.list_total_debts(user_id)
                quantity = debt_service.count_debts(user_id)

                user_menu(user_name, quantity, total_debts)
                option = input(">> ").strip()

                if option == "1":
                    total = safe_number("Total: ")
                    description = safe_text("Descripción: ")

                    result = debt_service.add_debt(user_id, total, description)
                    print("Resultado:", result)

                elif option == "2":
                    debts = debt_service.list_debts(user_id)

                    if not debts:
                        print("No hay deudas")
                    else:
                        draw_table(
                            "DEUDAS",
                            ["ID", "TOTAL", "PAGADO", "DESC"],
                            [(d[0], format_currency(d[2]), format_currency(d[3]), d[4]) for d in debts]
                        )

                elif option == "3":
                    debt_id = safe_int("ID deuda: ")
                    amount = safe_number("Monto: ")

                    result = payment_service.add_payment(debt_id, amount)
                    print("Abono:", result)

                elif option == "4":
                    debt_id = safe_int("ID deuda: ")

                    payments = payment_service.list_payments(user_id, debt_id)

                    if not payments:
                        print("No hay abonos")
                    else:
                        draw_table(
                            "ABONOS",
                            ["ID", "MONTO", "FECHA"],
                            [(p[0], format_currency(p[2]), p[3]) for p in payments]
                        )

                elif option == "5":
                    current_user = None

                else:
                    print("❌ Opción inválida")

                input("\nENTER para continuar...")

        except KeyboardInterrupt:
            print("\n👋 Saliendo...")
            break

        except Exception as e:
            print(f"🔥 Error inesperado: {e}")
            input("\nENTER para continuar...")
