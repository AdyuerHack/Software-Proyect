"""Juego de ahorcado en consola para practicar Python.

El programa permite jugar al clásico juego del ahorcado con una lista
predefinida de palabras o un fichero externo. Incluye manejo de
argumentos, validación de entradas y separación de responsabilidades en
funciones pequeñas para fomentar buenas prácticas.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Set

DEFAULT_WORDS = (
    "python",
    "funcion",
    "variable",
    "bucle",
    "condicional",
    "programacion",
    "desarrollo",
    "repositorio",
    "algoritmo",
    "depuracion",
)


@dataclass
class GameState:
    """Representa el estado actual de la partida."""

    secret_word: str
    guessed_letters: Set[str]
    attempts_left: int

    @property
    def masked_word(self) -> str:
        """Devuelve la palabra secreta mostrando guiones para letras no adivinadas."""

        return " ".join(
            letter if letter in self.guessed_letters else "_" for letter in self.secret_word
        )

    @property
    def is_won(self) -> bool:
        """Indica si todas las letras han sido adivinadas."""

        return set(self.secret_word).issubset(self.guessed_letters)

    @property
    def is_lost(self) -> bool:
        """Indica si se han agotado los intentos."""

        return self.attempts_left <= 0 and not self.is_won


def load_words(source: Path | None) -> list[str]:
    """Carga palabras desde un fichero de texto o usa la lista por defecto."""

    if source is None:
        return list(DEFAULT_WORDS)

    if not source.exists():
        raise FileNotFoundError(f"No se encontró el fichero de palabras: {source}")

    content = [line.strip().lower() for line in source.read_text(encoding="utf-8").splitlines()]
    words = [word for word in content if word.isalpha()]
    if not words:
        raise ValueError("El fichero de palabras no contiene entradas válidas")
    return words


def choose_secret_word(words: Iterable[str]) -> str:
    """Selecciona aleatoriamente una palabra secreta."""

    normalized = [word.strip().lower() for word in words if word.strip()]
    if not normalized:
        raise ValueError("La lista de palabras está vacía")
    return random.choice(normalized)


def request_letter(already_used: Set[str]) -> str:
    """Solicita una letra al usuario asegurándose de que sea válida."""

    while True:
        raw = input("Introduce una letra: ").strip().lower()
        if len(raw) != 1 or not raw.isalpha():
            print("⚠️  Debes introducir solo una letra.")
            continue
        if raw in already_used:
            print("⚠️  Ya usaste esa letra. Prueba con otra.")
            continue
        return raw


def update_game_state(state: GameState, guess: str) -> None:
    """Actualiza el estado de la partida en función de la letra indicada."""

    state.guessed_letters.add(guess)
    if guess not in state.secret_word:
        state.attempts_left -= 1
        print(f"La letra '{guess}' no está en la palabra. Intentos restantes: {state.attempts_left}")
    else:
        print("¡Bien! La letra está en la palabra.")


def print_status(state: GameState) -> None:
    """Muestra por pantalla la información relevante de la partida."""

    print("\nPalabra:", state.masked_word)
    print("Letras usadas:", " ".join(sorted(state.guessed_letters)) or "(ninguna)")
    print("Intentos restantes:", state.attempts_left)


def parse_args() -> argparse.Namespace:
    """Procesa los argumentos de línea de comandos."""

    parser = argparse.ArgumentParser(
        description="Juego clásico del ahorcado para practicar Python",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-w",
        "--word-file",
        type=Path,
        default=None,
        help="Ruta a un fichero de texto con palabras (una por línea)",
    )
    parser.add_argument(
        "-a",
        "--attempts",
        type=int,
        default=7,
        help="Número de intentos permitidos",
    )
    return parser.parse_args()


def main() -> None:
    """Punto de entrada del programa."""

    args = parse_args()
    words = load_words(args.word_file)
    secret = choose_secret_word(words)

    state = GameState(secret_word=secret, guessed_letters=set(), attempts_left=args.attempts)
    print("Bienvenido/a al juego del ahorcado. ¡Mucha suerte!")

    while not (state.is_won or state.is_lost):
        print_status(state)
        guess = request_letter(state.guessed_letters)
        update_game_state(state, guess)

    print_status(state)
    if state.is_won:
        print(f"🎉 ¡Felicidades! Adivinaste la palabra '{state.secret_word}'.")
    else:
        print(f"😢 Has perdido. La palabra era '{state.secret_word}'.")


if __name__ == "__main__":
    main()
