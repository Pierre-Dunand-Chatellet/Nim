"use strict";

const TOTAL_OBJECTS = 20;
const NIVEAUX = { 1: "Apprenti", 2: "Stratège", 3: "Imbattable" };

const screens = {
  menu: document.getElementById("screen-menu"),
  difficulty: document.getElementById("screen-difficulty"),
  game: document.getElementById("screen-game"),
};

const dotsGrid = document.getElementById("dots-grid");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");
const countDisplay = document.getElementById("count-display");
const turnLabel = document.getElementById("turn-label");
const gameInfo = document.getElementById("game-info");
const logMessage = document.getElementById("log-message");
const actionsRow = document.getElementById("actions-row");
const endPanel = document.getElementById("end-panel");
const replayBtn = document.getElementById("replay-btn");
const takeButtons = Array.from(document.querySelectorAll("[data-take]"));

for (let i = 0; i < TOTAL_OBJECTS; i++) {
  const dot = document.createElement("div");
  dot.className = "dot";
  dotsGrid.appendChild(dot);
}
const dotEls = Array.from(dotsGrid.children);

let state = null;

function showScreen(name) {
  Object.values(screens).forEach((s) => s.classList.remove("is-active"));
  screens[name].classList.add("is-active");
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// ── Logique IA (portage fidèle du jeux.py) ──────────────────────────────
function choixOrdinateur(nbObjet, difficulte) {
  if (difficulte === 1) {
    if (nbObjet <= 3) return nbObjet;
    return randInt(1, 3);
  }
  if (difficulte === 2) {
    if (nbObjet < 13) {
      const reste = nbObjet % 4;
      return reste === 0 ? randInt(1, 3) : reste;
    }
    return randInt(1, 3);
  }
  const reste = nbObjet % 4;
  return reste === 0 ? randInt(1, 3) : reste;
}

document.querySelectorAll("[data-action='pvp']").forEach((b) =>
  b.addEventListener("click", () => startGame("pvp"))
);
document.querySelectorAll("[data-action='show-difficulty']").forEach((b) =>
  b.addEventListener("click", () => showScreen("difficulty"))
);
document.querySelectorAll("[data-action='back-menu']").forEach((b) =>
  b.addEventListener("click", () => showScreen("menu"))
);
document.querySelectorAll("[data-action='quit']").forEach((b) =>
  b.addEventListener("click", () => showScreen("menu"))
);
document.querySelectorAll("[data-difficulty]").forEach((b) =>
  b.addEventListener("click", () => startGame("pvc", Number(b.dataset.difficulty)))
);
takeButtons.forEach((b) =>
  b.addEventListener("click", () => humanPlay(Number(b.dataset.take)))
);

function startGame(mode, difficulte) {
  const roles = { humain: null, ordinateur: null };
  if (mode === "pvc") {
    if (Math.random() < 0.5) {
      roles.humain = 1;
      roles.ordinateur = 2;
    } else {
      roles.humain = 2;
      roles.ordinateur = 1;
    }
  }

  state = {
    mode,
    difficulte,
    nbObjet: TOTAL_OBJECTS,
    joueur: 1,
    gameOver: false,
    humain: roles.humain,
    ordinateur: roles.ordinateur,
  };

  gameInfo.textContent =
    mode === "pvc"
      ? `Adversaire : ${NIVEAUX[difficulte]} (Joueur ${state.ordinateur})   |   Vous : Joueur ${state.humain}`
      : "Mode 2 joueurs en local";

  logMessage.textContent =
    mode === "pvc"
      ? state.humain === 1
        ? "La partie commence ! Vous êtes le Joueur 1, c'est à vous d'ouvrir le bal."
        : "La partie commence ! L'ordinateur est le Joueur 1, il prend la main en premier."
      : "La partie commence. Joueur 1, à vous l'honneur !";

  endPanel.hidden = true;
  actionsRow.classList.remove("is-hidden");

  showScreen("game");
  refresh();

  if (mode === "pvc" && state.joueur === state.ordinateur) {
    setTimeout(computerPlay, 1200);
  }
}

function refresh() {
  countDisplay.textContent = String(state.nbObjet);

  const filled = Math.round((state.nbObjet / TOTAL_OBJECTS) * 100);
  progressFill.style.width = `${filled}%`;
  progressText.textContent = `${state.nbObjet} / ${TOTAL_OBJECTS}`;

  dotEls.forEach((dot, i) => dot.classList.toggle("is-filled", i < state.nbObjet));

  if (!state.gameOver) {
    let who;
    if (state.mode === "pvc" && state.joueur === state.ordinateur) {
      who = "L'ordinateur analyse la table...";
    } else if (state.mode === "pvc") {
      who = "C'est votre tour, faites le bon choix !";
    } else {
      who = `À toi de jouer, Joueur ${state.joueur} !`;
    }
    turnLabel.textContent = who;
  }

  const isHuman =
    state.mode === "pvp" || (state.mode === "pvc" && state.joueur === state.humain);
  const enabled = isHuman && !state.gameOver;
  takeButtons.forEach((b) => (b.disabled = !enabled));
}

function humanPlay(n) {
  if (state.gameOver) return;
  if (n > state.nbObjet) {
    logMessage.textContent = `Impossible ! Il ne reste que ${state.nbObjet} objet(s).`;
    return;
  }
  const accord = n === 1 ? "objet" : "objets";
  const who = state.mode === "pvc" ? "Vous avez pris" : `Le Joueur ${state.joueur} a pris`;
  logMessage.textContent = `${who} ${n} ${accord}.`;
  applyMove(n);
}

function computerPlay() {
  if (state.gameOver) return;
  const n = Math.min(choixOrdinateur(state.nbObjet, state.difficulte), state.nbObjet);
  const accord = n === 1 ? "objet" : "objets";
  logMessage.textContent = `L'ordinateur a retiré ${n} ${accord}.`;
  applyMove(n);
}

function applyMove(n) {
  state.nbObjet -= n;
  if (state.nbObjet === 0) {
    refresh();
    endGame();
    return;
  }
  state.joueur = state.joueur === 1 ? 2 : 1;
  refresh();
  if (state.mode === "pvc" && state.joueur === state.ordinateur) {
    setTimeout(computerPlay, 900);
  }
}

function endGame() {
  state.gameOver = true;

  let msg, btnText;
  if (state.mode === "pvp") {
    msg = `Victoire éclatante du Joueur ${state.joueur} !`;
    btnText = "Match retour !";
  } else if (state.joueur === state.humain) {
    msg = "Félicitations, vous avez battu l'ordinateur !";
    btnText = "Rejouez contre lui";
  } else {
    msg = "Dommage... L'ordinateur a été plus malin cette fois.";
    btnText = "Prendre ma revanche";
  }

  turnLabel.textContent = "Partie terminée";
  logMessage.textContent = msg;
  takeButtons.forEach((b) => (b.disabled = true));

  replayBtn.textContent = btnText;
  endPanel.hidden = false;
}

replayBtn.addEventListener("click", () => startGame(state.mode, state.difficulte));
