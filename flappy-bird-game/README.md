# Juego estilo Flappy Bird (local)

Este mini proyecto está hecho con **HTML + CSS + JavaScript puro** para poder ejecutarse fácilmente en tu ordenador.

## Cómo abrirlo

1. Entra en la carpeta `flappy-bird-game`.
2. Haz doble clic en `index.html`.
3. Se abrirá en tu navegador y podrás jugar.

> Opcional (recomendado en algunos navegadores): abrirlo con un servidor local.

### Ejecutarlo con servidor local (opcional)

Si tienes Python instalado:

```bash
cd flappy-bird-game
python3 -m http.server 8000
```

Luego abre: `http://localhost:8000`

## Controles

- `Espacio` o clic/tap: el pájaro sube.
- Botón **Reiniciar partida**: vuelve a empezar.

## Características

- Puntuación en vivo.
- Mejor puntuación guardada en `localStorage`.
- Colisiones con tuberías y suelo.
