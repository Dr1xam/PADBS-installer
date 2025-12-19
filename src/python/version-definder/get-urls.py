import argparse
import sys
from parsers import PARSER_REGISTRY

def main():
    parser = argparse.ArgumentParser(description="Find versions for software.")
    parser.add_argument(
        "app", 
        help=f"Application name. Available: {', '.join(PARSER_REGISTRY.keys())}"
    )
    
    args = parser.parse_args()
    
    # Нормалізуємо ввід (переводимо в нижній регістр)
    app_name = args.app.lower()

    # --- ЛОГІКА get_versions ТЕПЕР ТУТ ---
    if app_name in PARSER_REGISTRY:
        # 1. Створюємо екземпляр парсера
        parser_instance = PARSER_REGISTRY[app_name]()
        
        # 2. Отримуємо список версій
        versions = parser_instance.get_versions()
        
        # 3. Виводимо результат (у стовпчик)
        for v in versions:
            print(v)
            
    else:
        # Якщо програми немає в реєстрі
        print(f"Unknown application: {args.app}")
        sys.exit(1)

if __name__ == "__main__":
    main()
