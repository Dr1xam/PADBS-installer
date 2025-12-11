#!/bin/bash

# ЗМІННІ ШЛЯХІВ
# Тут ми визначаємо, куди мають бути розпаковані архіви
SOFTWARE_DIR="./resources/software"
TAR_GZ_DIR="./resources/software/tar_gz"

# --- РОЗПАКУВАННЯ PIP ---
# Перевіряємо, чи НЕ існує каталог $SOFTWARE_DIR/pip
if [ ! -d "$SOFTWARE_DIR/pip" ]; then
    echo "Розпакування PIP..."
    # Розпаковуємо архів PIP в папку $SOFTWARE_DIR
    tar -xzvf "$TAR_GZ_DIR/pip.tar.gz" -C "$SOFTWARE_DIR/"
else
    echo "Каталог $SOFTWARE_DIR/pip вже існує. Пропускаємо розпакування PIP."
fi

# --- РОЗПАКУВАННЯ ANSIBLE ---
# Перевіряємо, чи НЕ існує каталог $SOFTWARE_DIR/ansible
if [ ! -d "$SOFTWARE_DIR/ansible" ]; then
    echo "Розпакування ANSIBLE..."
    # Розпаковуємо архів ANSIBLE в папку $SOFTWARE_DIR
    tar -xzvf "$TAR_GZ_DIR/ansible.tar.gz" -C "$SOFTWARE_DIR/"
else
    echo "Каталог $SOFTWARE_DIR/ansible вже існує. Пропускаємо розпакування ANSIBLE."
fi
