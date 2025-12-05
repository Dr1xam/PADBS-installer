#!/bin/bash

PROJECT_DIR="./version_definder"

# Перевірка whiptail
if ! command -v whiptail &> /dev/null; then
    echo "Помилка: whiptail не встановлено."
    exit 1
fi

# ==============================================================================
# 1. ЗАВАНТАЖЕННЯ ДАНИХ (ПАРАЛЕЛЬНО)
# ==============================================================================

TMP_UBUNTU=$(mktemp)
TMP_ROCKET=$(mktemp)
TMP_ZABBIX=$(mktemp)

{
    python3 "$PROJECT_DIR/main.py" ubuntu > "$TMP_UBUNTU" &
    python3 "$PROJECT_DIR/main.py" rocketchat > "$TMP_ROCKET" &
    python3 "$PROJECT_DIR/main.py" zabbix > "$TMP_ZABBIX" &
    wait
} | whiptail --gauge "Завантаження списків версій..." 6 50 0

# ==============================================================================
# 2. ОБРОБКА ДАНИХ
# ==============================================================================

declare -A MAP_UBUNTU
declare -A MAP_ROCKET
declare -A MAP_ZABBIX
MENU_UBUNTU=()
MENU_ROCKET=()
MENU_ZABBIX=()

load_data() {
    local file="$1"
    declare -n menu_ref="$2"
    declare -n map_ref="$3"

    while read -r VER LINK; do
        if [[ -n "$VER" ]]; then
            menu_ref+=("$VER" "" "OFF")
            map_ref["$VER"]="$LINK"
        fi
    done < "$file"
}

load_data "$TMP_UBUNTU" MENU_UBUNTU MAP_UBUNTU
load_data "$TMP_ROCKET" MENU_ROCKET MAP_ROCKET
load_data "$TMP_ZABBIX" MENU_ZABBIX MAP_ZABBIX

rm "$TMP_UBUNTU" "$TMP_ROCKET" "$TMP_ZABBIX"

# ==============================================================================
# 3. ГОЛОВНЕ МЕНЮ (ЦИКЛ ПЕРЕВІРКИ)
# ==============================================================================

while true; do
    RAW_APPS=$(whiptail --title "Вибір програм" --checklist \
    "Що будемо встановлювати? (Оберіть мінімум одне)" 15 60 5 \
    "RocketChat" "Чат + Ubuntu" OFF \
    "Zabbix"     "Моніторинг" OFF \
    3>&1 1>&2 2>&3)

    # Перевірка кнопки Cancel/Esc
    if [ $? -ne 0 ]; then
        echo "Вихід користувачем."
        exit 0
    fi

    # Перевірка на порожній вибір
    if [ -n "$RAW_APPS" ]; then
        # Якщо НЕ порожньо — виходимо з циклу і йдемо далі
        break
    else
        # Якщо порожньо — показуємо помилку і цикл повторюється
        whiptail --title "Помилка" --msgbox "Ви нічого не вибрали!\nБудь ласка, відмітьте програму пробілом." 8 45
    fi
done

SELECTED_APPS_STR=$(echo $RAW_APPS | tr -d '"')

# ==============================================================================
# 4. МЕНЮ ВИБОРУ ВЕРСІЙ (ТЕЖ З ПЕРЕВІРКОЮ)
# ==============================================================================

# Функція для вибору з обов'язковою перевіркою
# Використання: safe_select "Заголовок" "Текст" "Масив_Меню" "Змінна_Результату"
safe_select() {
    local title="$1"
    local text="$2"
    declare -n menu_opts="$3" # Отримуємо масив за посиланням
    local result_var="$4"     # Назва змінної куди писати результат
    local selection=""

    while true; do
        selection=$(whiptail --title "$title" --radiolist \
        "$text" 20 60 10 \
        "${menu_opts[@]}" 3>&1 1>&2 2>&3)

        if [ $? -ne 0 ]; then
            echo "Вихід користувачем."
            exit 0
        fi

        if [ -n "$selection" ]; then
            break
        else
            whiptail --msgbox "Необхідно вибрати версію!" 8 40
        fi
    done

    # Повертаємо значення у глобальну змінну
    eval "$result_var=\"$selection\""
}

# --- ROCKET CHAT ---
if [[ "$SELECTED_APPS_STR" == *"RocketChat"* ]]; then
    # Використовуємо нашу нову функцію safe_select
    safe_select "Rocket.Chat OS" "Оберіть Ubuntu Base:" MENU_UBUNTU VER_UBUNTU
    safe_select "Rocket.Chat App" "Оберіть версію Rocket.Chat:" MENU_ROCKET VER_ROCKET
fi

# --- ZABBIX ---
if [[ "$SELECTED_APPS_STR" == *"Zabbix"* ]]; then
    safe_select "Zabbix Version" "Оберіть версію Zabbix:" MENU_ZABBIX VER_ZABBIX
fi

# ==============================================================================
# 5. ФІНАЛ
# ==============================================================================
clear
echo "========================================="
echo "           ГОТОВНІСТЬ ДО ВСТАНОВЛЕННЯ    "
echo "========================================="

if [[ "$SELECTED_APPS_STR" == *"RocketChat"* ]]; then
    LINK_UB="${MAP_UBUNTU[$VER_UBUNTU]}"
    LINK_RC="${MAP_ROCKET[$VER_ROCKET]}"
    
    echo " [ROCKETCHAT]"
    echo "   -> Ubuntu: $VER_UBUNTU ($LINK_UB)"
    echo "   -> App:    $VER_ROCKET ($LINK_RC)"
fi

if [[ "$SELECTED_APPS_STR" == *"Zabbix"* ]]; then
    LINK_ZB="${MAP_ZABBIX[$VER_ZABBIX]}"
    
    echo " [ZABBIX]"
    echo "   -> App:    $VER_ZABBIX ($LINK_ZB)"
fi
echo ""
