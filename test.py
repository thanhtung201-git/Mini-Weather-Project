from rich.console import Console
from rich.table import Table

console = Console()

def show_menu():
    table = Table(title="🌦️ MENU DỰ BÁO THỜI TIẾT", show_lines=True)
    table.add_column("Lựa chọn", justify="center")
    table.add_column("Chức năng")

    table.add_row("1", "Biểu đồ nhiệt độ")
    table.add_row("2", "Biểu đồ độ ẩm")
    table.add_row("3", "Biểu đồ gió")
    table.add_row("4", "Biểu đồ loại thời tiết (pie)")
    table.add_row("0", "Thoát")

    console.print(table)

# Gọi
while True:
    show_menu()
    choice = input("👉 Nhập lựa chọn (0-4): ")
    ...
from rich.console import Console
from rich.table import Table

console = Console()

def show_menu():
    table = Table(title="🌦️ MENU DỰ BÁO THỜI TIẾT", show_lines=True)
    table.add_column("Lựa chọn", justify="center")
    table.add_column("Chức năng")

    table.add_row("1", "Biểu đồ nhiệt độ")
    table.add_row("2", "Biểu đồ độ ẩm")
    table.add_row("3", "Biểu đồ gió")
    table.add_row("4", "Biểu đồ loại thời tiết (pie)")
    table.add_row("0", "Thoát")

    console.print(table)

# Gọi