"use strict";

// portage web du jeu de Nim que j'avais fait en Python (Tkinter) au départ.
// mêmes règles, même IA, juste réécrit pour tourner dans le navigateur.

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

// je génère les 20 ronds en JS plutôt que de les coder en dur dans le HTML,
// comme ça si un jour je change TOTAL_OBJECTS le plateau suit tout seul
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
// le truc à comprendre sur le Nim : avec un max de 3 objets par tour, une pile
// multiple de 4 est perdante pour celui qui doit jouer (quoi qu'il prenne, l'autre
// ramène toujours sur le prochain multiple de 4). donc "jouer parfait" = toujours
// laisser un multiple de 4 à l'adversaire.
function choixOrdinateur(nbObjet, difficulte) {
  if (difficulte === 1) {
    // Apprenti : joue au hasard, mais finit la partie s'il peut (sinon ça traîne)
    if (nbObjet <= 3) return nbObjet;
    return randInt(1, 3);
  }
  if (difficulte === 2) {
    // Stratège : hasard tant qu'il reste beaucoup d'objets, calcule en dessous de 13
    if (nbObjet < 13) {
      const reste = nbObjet % 4;
      return reste === 0 ? randInt(1, 3) : reste;
    }
    return randInt(1, 3);
  }
  // Imbattable : applique la stratégie optimale du début à la fin
  const reste = nbObjet % 4;
  return reste === 0 ? randInt(1, 3) : reste;
}

// tous les boutons du menu / difficulté sont branchés via des data-attributes
// plutôt que des id un par un, ça évite d'oublier un bouton si j'en rajoute
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
  // le joueur 1 ouvre toujours la partie, mais qui EST le joueur 1 (humain ou
  // ordi) est tiré au sort à chaque partie — sinon l'ordi aurait toujours
  // l'avantage (ou toujours le désavantage) d'ouvrir, ce qui serait pas fair-play
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

  // si l'ordi commence, il faut déclencher son coup nous-mêmes (sinon rien
  // ne se passe, personne n'a cliqué). petit délai pour que ça paraisse
  // moins instantané/robotique
  if (mode === "pvc" && state.joueur === state.ordinateur) {
    setTimeout(computerPlay, 1200);
  }
}

// remet à jour tout l'affichage à partir de state — appelée après chaque coup
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
  // règle du jeu : celui qui prend le DERNIER objet gagne, donc dès qu'il
  // n'en reste plus, la partie est finie et c'est le joueur qui vient de
  // jouer qui a gagné
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
