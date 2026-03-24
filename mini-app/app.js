const webApp = window.Telegram.WebApp;
webApp.ready(); // signal that the app loaded

// Get the Telegram user who opened the app
const user = webApp.initDataUnsafe.user;

// Adapt to user's Telegram theme (dark/light)
document.body.style.backgroundColor = webApp.backgroundColor;

// Main action button at the bottom
webApp.MainButton.setText("Register for Game");
webApp.MainButton.show();
webApp.MainButton.onClick(() => {
  webApp.sendData(JSON.stringify({ action: "register", userId: user.id }));
});