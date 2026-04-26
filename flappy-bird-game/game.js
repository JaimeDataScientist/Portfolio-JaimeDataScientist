const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");
const bestScoreEl = document.getElementById("bestScore");
const restartBtn = document.getElementById("restartBtn");

const GRAVITY = 0.45;
const JUMP_FORCE = -7.2;
const PIPE_SPEED = 2.4;
const PIPE_GAP = 160;
const PIPE_INTERVAL = 1400;
const GROUND_HEIGHT = 95;

let bird;
let pipes;
let score;
let bestScore = Number(localStorage.getItem("flappyBest")) || 0;
let gameOver;
let started;
let lastPipeTime;
let animationId;

function resetGame() {
  bird = {
    x: 100,
    y: canvas.height / 2,
    radius: 16,
    velocity: 0,
    rotation: 0,
  };

  pipes = [];
  score = 0;
  gameOver = false;
  started = false;
  lastPipeTime = performance.now();
  scoreEl.textContent = "0";
  bestScoreEl.textContent = String(bestScore);

  if (animationId) {
    cancelAnimationFrame(animationId);
  }

  loop(performance.now());
}

function flap() {
  if (gameOver) {
    return;
  }

  started = true;
  bird.velocity = JUMP_FORCE;
}

function createPipe(now) {
  if (now - lastPipeTime < PIPE_INTERVAL) {
    return;
  }

  const minTop = 60;
  const maxTop = canvas.height - GROUND_HEIGHT - PIPE_GAP - 60;
  const topHeight = Math.floor(Math.random() * (maxTop - minTop + 1)) + minTop;

  pipes.push({
    x: canvas.width + 40,
    width: 62,
    top: topHeight,
    passed: false,
  });

  lastPipeTime = now;
}

function update() {
  if (!started || gameOver) {
    return;
  }

  bird.velocity += GRAVITY;
  bird.y += bird.velocity;
  bird.rotation = Math.max(-0.45, Math.min(0.9, bird.velocity / 10));

  pipes.forEach((pipe) => {
    pipe.x -= PIPE_SPEED;

    if (!pipe.passed && pipe.x + pipe.width < bird.x - bird.radius) {
      pipe.passed = true;
      score += 1;
      scoreEl.textContent = String(score);
    }
  });

  pipes = pipes.filter((pipe) => pipe.x + pipe.width > -5);

  if (bird.y + bird.radius >= canvas.height - GROUND_HEIGHT || bird.y - bird.radius <= 0) {
    endGame();
  }

  for (const pipe of pipes) {
    const withinX = bird.x + bird.radius > pipe.x && bird.x - bird.radius < pipe.x + pipe.width;
    const hitTop = bird.y - bird.radius < pipe.top;
    const hitBottom = bird.y + bird.radius > pipe.top + PIPE_GAP;

    if (withinX && (hitTop || hitBottom)) {
      endGame();
      break;
    }
  }
}

function endGame() {
  gameOver = true;
  if (score > bestScore) {
    bestScore = score;
    localStorage.setItem("flappyBest", String(bestScore));
    bestScoreEl.textContent = String(bestScore);
  }
}

function drawBird() {
  ctx.save();
  ctx.translate(bird.x, bird.y);
  ctx.rotate(bird.rotation);

  ctx.fillStyle = "#ffe36e";
  ctx.beginPath();
  ctx.arc(0, 0, bird.radius, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#f89f34";
  ctx.beginPath();
  ctx.moveTo(12, 0);
  ctx.lineTo(24, 5);
  ctx.lineTo(24, -5);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#111";
  ctx.beginPath();
  ctx.arc(4, -5, 3.2, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

function drawPipes() {
  ctx.fillStyle = "#3eaf48";
  ctx.strokeStyle = "#26762c";

  pipes.forEach((pipe) => {
    ctx.fillRect(pipe.x, 0, pipe.width, pipe.top);
    ctx.strokeRect(pipe.x, 0, pipe.width, pipe.top);

    const bottomY = pipe.top + PIPE_GAP;
    const bottomHeight = canvas.height - GROUND_HEIGHT - bottomY;
    ctx.fillRect(pipe.x, bottomY, pipe.width, bottomHeight);
    ctx.strokeRect(pipe.x, bottomY, pipe.width, bottomHeight);
  });
}

function drawBackground() {
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#87ceeb");
  gradient.addColorStop(1, "#c9efff");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#8cd96b";
  ctx.fillRect(0, canvas.height - GROUND_HEIGHT, canvas.width, GROUND_HEIGHT);
}

function drawOverlay() {
  if (!started && !gameOver) {
    drawText("Pulsa Espacio o clic", canvas.height / 2 - 10, 28);
    drawText("para empezar", canvas.height / 2 + 28, 24);
  }

  if (gameOver) {
    drawText("¡Game Over!", canvas.height / 2 - 22, 42);
    drawText("Reinicia para jugar otra vez", canvas.height / 2 + 24, 22);
  }
}

function drawText(text, y, size) {
  ctx.font = `bold ${size}px Arial`;
  ctx.textAlign = "center";
  ctx.lineWidth = 4;
  ctx.strokeStyle = "rgba(0, 0, 0, 0.35)";
  ctx.strokeText(text, canvas.width / 2, y);
  ctx.fillStyle = "white";
  ctx.fillText(text, canvas.width / 2, y);
}

function render() {
  drawBackground();
  drawPipes();
  drawBird();
  drawOverlay();
}

function loop(now) {
  createPipe(now);
  update();
  render();
  animationId = requestAnimationFrame(loop);
}

window.addEventListener("keydown", (event) => {
  if (event.code === "Space") {
    event.preventDefault();
    flap();
  }
});

canvas.addEventListener("pointerdown", flap);
restartBtn.addEventListener("click", resetGame);

bestScoreEl.textContent = String(bestScore);
resetGame();
