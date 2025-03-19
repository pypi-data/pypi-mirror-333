{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyObpFtvPFdmTn4sfpKwgOkm",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/TheAmirHK/bb84_crypto/blob/main/bb84_crypto/bb84_py.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "Uq7umCKy5F_y"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import os\n",
        "\n",
        "def generate_random_bits(n):\n",
        "    return np.random.randint(2, size=n)\n",
        "\n",
        "def generate_random_bases(n):\n",
        "    return np.random.randint(2, size=n)\n",
        "\n",
        "def encode_qubits(bits, bases):\n",
        "    return [(bit, base) for bit, base in zip(bits, bases)]\n",
        "\n",
        "def measure_qubits(qubits, measurement_bases):\n",
        "    measured_bits = []\n",
        "    for (bit, base), measure_base in zip(qubits, measurement_bases):\n",
        "        if base == measure_base:\n",
        "            measured_bits.append(bit)\n",
        "        else:\n",
        "            measured_bits.append(np.random.randint(2))\n",
        "    return measured_bits\n",
        "\n",
        "def sift_key(alice_bases, bob_bases, alice_bits, bob_bits):\n",
        "    return [alice_bits[i] for i in range(len(alice_bits)) if alice_bases[i] == bob_bases[i]]\n",
        "\n",
        "def bb84_protocol(n=100):\n",
        "    alice_bits = generate_random_bits(n)\n",
        "    alice_bases = generate_random_bases(n)\n",
        "\n",
        "    qubits = encode_qubits(alice_bits, alice_bases)\n",
        "\n",
        "    bob_bases = generate_random_bases(n)\n",
        "    bob_bits = measure_qubits(qubits, bob_bases)\n",
        "\n",
        "    return sift_key(alice_bases, bob_bases, alice_bits, bob_bits)\n",
        "\n",
        "def binary_to_text(binary_str):\n",
        "    chars = [chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)]\n",
        "    return ''.join(chars)\n",
        "\n",
        "def text_to_binary(text):\n",
        "    return ''.join(format(ord(c), '08b') for c in text)\n",
        "\n",
        "def encrypt_message(message, key):\n",
        "    message_bits = text_to_binary(message)\n",
        "\n",
        "    if len(key) < len(message_bits):\n",
        "        key.extend(generate_random_bits(len(message_bits) - len(key)))\n",
        "\n",
        "    key_bits = ''.join(map(str, key[:len(message_bits)]))\n",
        "    encrypted_bits = ''.join(str(int(m) ^ int(k)) for m, k in zip(message_bits, key_bits))\n",
        "    return encrypted_bits\n",
        "\n",
        "def decrypt_message(encrypted_bits, key):\n",
        "    key_bits = ''.join(map(str, key[:len(encrypted_bits)]))\n",
        "    decrypted_bits = ''.join(str(int(e) ^ int(k)) for e, k in zip(encrypted_bits, key_bits))\n",
        "    return binary_to_text(decrypted_bits)"
      ]
    }
  ]
}
