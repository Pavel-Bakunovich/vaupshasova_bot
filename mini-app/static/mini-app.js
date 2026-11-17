// Initialize Telegram WebApp
const webApp = window.Telegram.WebApp;
webApp.ready();
webApp.expand();
// Stop vertical swipes inside the app from minimizing/closing the mini-app
// (Bot API 7.7+). The app can still be closed from Telegram's header.
if (typeof webApp.disableVerticalSwipes === 'function') {
    webApp.disableVerticalSwipes();
}

// Get user data from Telegram (or mock for testing)
let user = webApp.initDataUnsafe?.user;
if (!user || !user.id) {
    // Mock user for browser testing
    user = { id: 343151297, first_name: 'Паша', last_name: 'Бакунович Тест' };
    console.log('Using mock user for testing:', user);
}
let currentPlayerData = null;

// Initialization
document.addEventListener('DOMContentLoaded', function() {
    if (user && user.id) {
        initializeApp();
    } else {
        console.error('Cannot get user from Telegram');
    }
});

async function initializeApp() {
    await loadPlayerData();
    await loadSquadList();
}

async function loadPlayerData() {
    try {
        const response = await fetch(`/api/player/${user.id}`);
        if (!response.ok) throw new Error('Failed to load player data');
        
        const data = await response.json();
        if (data.success) {
            currentPlayerData = data.player;
            updatePlayerDisplay(data.player, data.stats, data.season_stats, data.current_year, data.attendance_streak);
            updateBalance(data.balance);
            await loadPerformance();
        }
    } catch (error) {
        console.error('Error loading player data:', error);
        document.getElementById('player-greeting').textContent = 'Ошибка загрузки';
    }
}

async function loadPerformance() {
    if (!currentPlayerData) return;
    
    try {
        const response = await fetch(`/api/player/${currentPlayerData.id}/last-games-performance`);
        if (!response.ok) throw new Error('Failed to load performance');
        
        const data = await response.json();
        if (data.success) {
            displayPerformance(data.performance);
        }
    } catch (error) {
        console.error('Error loading performance:', error);
    }
}

function displayPerformance(performance) {
    const container = document.getElementById('performance-squares');
    container.innerHTML = '';
    
    for (const result of performance) {
        const square = document.createElement('div');
        square.className = 'performance-square';
        square.textContent = result;
        
        if (result === 'W') {
            square.classList.add('win');
        } else if (result === 'D') {
            square.classList.add('draw');
        } else if (result === 'L') {
            square.classList.add('loss');
        }
        
        container.appendChild(square);
    }
}

function updatePlayerDisplay(player, stats, season_stats, current_year, attendanceStreak) {
    // Get display name (prefer friendly name)
    const displayName = `${player.friendly_first_name || player.first_name} ${player.friendly_last_name || player.last_name}`;
    
    document.getElementById('player-greeting').textContent = `Привет, ${displayName}`;
    const attendanceStreakElement = document.getElementById('attendance-streak');
    attendanceStreakElement.hidden = !attendanceStreak;
    if (attendanceStreak) {
        document.getElementById('attendance-streak-label').textContent = attendanceStreak.played
            ? 'Игр сыграно подряд:'
            : 'Пропустил игр подряд:';
        document.getElementById('attendance-streak-count').textContent = attendanceStreak.count;
    }
    document.getElementById('season-header').textContent = `Сезон ${current_year}`;
    document.getElementById('season-games').textContent = season_stats.games_played;
    document.getElementById('season-goals').textContent = season_stats.goals;
    document.getElementById('season-assists').textContent = season_stats.assists;
    document.getElementById('season-own-goals').textContent = season_stats.own_goals;
    
    // Update other screens with player name
    document.getElementById('alltime-stats-header').textContent = displayName;
    document.getElementById('season-stats-player-name').textContent = displayName;
    document.getElementById('balance-name').textContent = displayName;
    
    // Load detailed stats
    loadAlltimeStats();
    loadSeasonStats();
    loadPersonalStats();
}

function updateBalance(balance) {
    const balanceElement = document.getElementById('balance-value');
    let sign = balance >= 0 ? '+' : '';
    let colorClass = balance >= 0 ? 'positive' : 'negative';
    balanceElement.innerHTML = `<span class="${colorClass}">${sign}${balance} р.</span>`;
}

async function loadSquadList() {
    try {
        const response = await fetch(`/api/next-matchday-squad/${user.id}`);
        if (!response.ok) throw new Error('Failed to load squad');
        
        const data = await response.json();
        if (data.success) {
            displaySquadList(data.squad_add, data.squad_chair, data.squad_maybe, data.squad_remove);
            document.getElementById('next-matchday-date').textContent = `📋 Следующая игра 🗓️ ${data.next_matchday_date}`;
        }
    } catch (error) {
        console.error('Error loading squad:', error);
    }
}

function displaySquadList(squadAdd, squadChair, squadMaybe, squadRemove) {
    const squadList = document.getElementById('squad-list');
    let html = '';
    
    // Display 12 numbered slots for "add" registration type
    const slotCount = 12;
    const numberEmojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'];
    
    function getNumberDisplay(num) {
        // num is 1-12, display as 01-12 with emojis
        const firstDigit = Math.floor(num / 10);
        const secondDigit = num % 10;
        return numberEmojis[firstDigit] + numberEmojis[secondDigit];
    }

    function formatTimeStamp(timestamp) {
        if (!timestamp) return '';
        const parsed = new Date(timestamp);
        if (Number.isNaN(parsed.getTime())) {
            return timestamp;
        }

        const day = String(parsed.getDate()).padStart(2, '0');
        const monthNames = ['Янв', 'Фев', 'Мар', 'Апр', 'Мая', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
        const month = monthNames[parsed.getMonth()];
        const hours = String(parsed.getHours()).padStart(2, '0');
        const minutes = String(parsed.getMinutes()).padStart(2, '0');
        return `${day} ${month}, ${hours}:${minutes}`;
    }
    
    for (let i = 0; i < slotCount; i++) {
        const player = squadAdd[i];
        const slotNumber = getNumberDisplay(i + 1);
        
        const isCurrentUser = player && player.is_current_user;
        const borderClass = isCurrentUser ? 'current-user' : '';
        
        if (player) {
            const displayName = `${player.friendly_first_name} ${player.friendly_last_name}`;
            const squadEmoji = player.squad_emoji || '';
            html += `
                <div class="squad-slot ${borderClass}">
                    <div class="slot-number">${slotNumber}</div>
                    <div class="slot-content">
                        ${squadEmoji ? '<span class="squad-emoji">' + squadEmoji + '</span>' : ''}
                        <span class="player-name">${displayName}</span>
                        <span class="timestamp">${formatTimeStamp(player.time_stamp)}</span>
                    </div>
                </div>
            `;
        } else {
            html += `
                <div class="squad-slot empty">
                    <div class="slot-number">${slotNumber}</div>
                    <div class="slot-content">
                        <span class="player-name">—</span>
                    </div>
                </div>
            `;
        }
    }
    
    // Display chair players if any
    if (squadChair && squadChair.length > 0) {
        for (const player of squadChair) {
            const displayName = `${player.friendly_first_name} ${player.friendly_last_name}`;
            const isCurrentUser = player.is_current_user;
            const borderClass = isCurrentUser ? 'current-user' : '';
            html += `
                <div class="squad-slot other-category ${borderClass}">
                    <div class="slot-emoji">🪑</div>
                    <div class="slot-content">
                        <span class="player-name">${displayName}</span>
                        <span class="timestamp">${formatTimeStamp(player.time_stamp)}</span>
                    </div>
                </div>
            `;
        }
    }
    
    // Display maybe players if any
    if (squadMaybe && squadMaybe.length > 0) {
        for (const player of squadMaybe) {
            const displayName = `${player.friendly_first_name} ${player.friendly_last_name}`;
            const isCurrentUser = player.is_current_user;
            const borderClass = isCurrentUser ? 'current-user' : '';
            html += `
                <div class="squad-slot other-category ${borderClass}">
                    <div class="slot-emoji">❓</div>
                    <div class="slot-content">
                        <span class="player-name">${displayName}</span>
                        <span class="timestamp">${formatTimeStamp(player.time_stamp) || ''}</span>
                    </div>
                </div>
            `;
        }
    }
    
    // Display remove players if any
    if (squadRemove && squadRemove.length > 0) {
        for (const player of squadRemove) {
            const displayName = `${player.friendly_first_name} ${player.friendly_last_name}`;
            const isCurrentUser = player.is_current_user;
            const borderClass = isCurrentUser ? 'current-user' : '';
            html += `
                <div class="squad-slot other-category ${borderClass}">
                    <div class="slot-emoji">❌</div>
                    <div class="slot-content">
                        <span class="player-name">${displayName}</span>
                        <span class="timestamp">${formatTimeStamp(player.time_stamp) || ''}</span>
                    </div>
                </div>
            `;
        }
    }
    
    if (!squadAdd || squadAdd.length === 0) {
        html = '<div class="loading">На данный момент никто не зарегистрирован</div>';
    }
    
    squadList.innerHTML = html;
}

async function loadAlltimeStats() {
    if (!currentPlayerData) return;
    
    try {
        const response = await fetch(`/api/player/${user.id}`);
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            document.getElementById('alltime-games').textContent = stats.games_played;
            document.getElementById('alltime-goals').textContent = stats.goals;
            document.getElementById('alltime-assists').textContent = stats.assists;
            document.getElementById('alltime-own-goals').textContent = stats.own_goals;
            document.getElementById('total-games-for-corn').textContent = stats.games_for_corn;
            document.getElementById('total-games-for-tomato').textContent = stats.games_for_tomato;
        }
        
        // Load streaks
        const streaksResponse = await fetch(`/api/player/${currentPlayerData.id}/streaks`);
        const streaksData = await streaksResponse.json();
        
        if (streaksData.success) {
            document.getElementById('win-streak').textContent = streaksData.win_streak;
            document.getElementById('loss-streak').textContent = streaksData.loss_streak;
        }
    } catch (error) {
        console.error('Error loading alltime stats:', error);
    }
}

async function loadSeasonStats() {
    try {
        const response = await fetch('/api/current-season-stats');
        const data = await response.json();
        
        if (data.success) {
            // Update season score
            document.getElementById('corn-wins').textContent = data.season_score.corn_wins;
            document.getElementById('draws').textContent = data.season_score.draws;
            document.getElementById('tomato-wins').textContent = data.season_score.tomato_wins;
            
            // Update header with current year
            document.getElementById('season-stats-name').textContent = `📈 Статистика сезона ${data.year}`;
            
            // Update player stats table
            const tbody = document.getElementById('season-stats-body');
            tbody.innerHTML = data.players.map(player => `
                <tr>
                    <td>${player.rank}</td>
                    <td>${player.first_name} ${player.last_name}</td>
                    <td>${player.games_played}</td>
                    <td>${player.goals}</td>
                    <td>${player.assists}</td>
                    <td>${player.own_goals}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading season stats:', error);
    }
}

async function loadPersonalStats() {
    if (!currentPlayerData) return;
    
    const content = document.getElementById('personal-stats-content');
    
    try {
        const response = await fetch(`/api/player/${user.id}`);
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            content.innerHTML = `
                <h2 class="section-title">📊 Основная статистика</h2>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-label">Всего игр</div>
                        <div class="stat-value">${stats.games_played}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Всего голов</div>
                        <div class="stat-value">${stats.goals}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Всего асистов</div>
                        <div class="stat-value">${stats.assists}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Автоголы</div>
                        <div class="stat-value">${stats.own_goals}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">За Кукурузу</div>
                        <div class="stat-value">${stats.games_for_corn}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">За Помидор</div>
                        <div class="stat-value">${stats.games_for_tomato}</div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading personal stats:', error);
        content.innerHTML = '<div class="error">Ошибка при загрузке статистики</div>';
    }
}

function formatMoney(amount, withSign = false) {
    const sign = withSign && amount > 0 ? '+' : '';
    return `${sign}${amount} р.`;
}

function moneyClass(amount) {
    return amount > 0 ? 'positive' : amount < 0 ? 'negative' : 'neutral';
}

async function loadBalanceData() {
    if (!currentPlayerData) return;

    const amountItem = document.getElementById('balance-amount-item');
    const content = document.getElementById('balance-history-content');
    content.innerHTML = '<div class="loading">Загрузка...</div>';

    try {
        const response = await fetch(`/api/player/${currentPlayerData.id}/balance`);
        const data = await response.json();
        if (!data.success) throw new Error(data.error || 'Failed to load balance');

        const balanceAmount = data.balance || 0;
        amountItem.classList.remove('positive', 'negative', 'neutral');
        amountItem.classList.add(moneyClass(balanceAmount));
        document.getElementById('balance-amount').textContent = formatMoney(balanceAmount, true);
        document.getElementById('balance-total-paid').textContent = formatMoney(data.total_paid || 0);

        if (!data.history || data.history.length === 0) {
            content.innerHTML = '<div class="loading">Платежей пока нет</div>';
            return;
        }

        let html = `<div class="table-responsive"><table class="stat-table balance-table"><thead><tr>
            <th>Дата</th><th>Сдал</th><th>Изменение баланса</th><th>Баланс на дату</th>
        </tr></thead><tbody>`;
        data.history.forEach(item => {
            html += `<tr>
                <td class="date-col">${item.date || '—'}</td>
                <td>${formatMoney(item.money_given)}</td>
                <td class="${moneyClass(item.balance_change)}">${formatMoney(item.balance_change, true)}</td>
                <td class="${moneyClass(item.balance_by_date)}">${formatMoney(item.balance_by_date, true)}</td>
            </tr>`;
        });
        html += '</tbody></table></div>';
        content.innerHTML = html;
    } catch (error) {
        console.error('Error loading balance:', error);
        content.innerHTML = '<div class="error">Ошибка при загрузке баланса</div>';
    }
}

async function registerAction(action) {
    try {
        const response = await fetch('/api/register-player-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                telegram_id: user.id,
                action: action
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show success message
            alert('Эта кнопка пока не работает ❌');
            // Reload squad list
            loadSquadList();
        } else {
            alert('❌ Ошибка: ' + (data.error || 'Неизвестная ошибка'));
        }
    } catch (error) {
        console.error('Error registering action:', error);
        alert('❌ Ошибка при регистрации');
    }
}

function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show selected screen
    document.getElementById(screenId).classList.add('active');

    // All screens share the same document scroll, so reset it —
    // otherwise the new screen opens at the previous screen's scroll offset
    window.scrollTo(0, 0);

    // Load data for specific screens
    if (screenId === 'balance-screen') {
        loadBalanceData();
    } else if (screenId === 'season-stats-screen') {
        loadSeasonStats();
    } else if (screenId === 'alltime-stats-screen') {
        loadAlltimeStatsTable();
    } else if (screenId === 'games-log-screen') {
        loadGamesLog();
    }
}

async function loadGamesLog() {
    const content = document.getElementById('games-log-content');
    try {
        const playerParam = currentPlayerData && currentPlayerData.id ? `?player_id=${currentPlayerData.id}` : '';
        const response = await fetch(`/api/games-log${playerParam}`);
        const data = await response.json();
        if (!data.success) throw new Error(data.error || 'Failed to load games log');

        document.getElementById('games-log-header').textContent = `Всего игр: ${data.games.length}`;

        if (data.games.length === 0) {
            content.innerHTML = '<div class="loading">Игр пока нет</div>';
            return;
        }

        let html = `<div class="table-responsive"><table class="stat-table games-log-table"><thead><tr>
            <th>Дата</th><th class="team-col">Кукуруза</th><th class="score-col">Счёт</th><th class="team-col">Помидоры</th><th>Лучший бомбардир</th><th class="played-col">Я играл</th>
        </tr></thead><tbody>`;
        data.games.forEach(game => {
            const cornScore = game.score_corn > game.score_tomato ? `<b>${game.score_corn}</b>` : game.score_corn;
            const tomatoScore = game.score_tomato > game.score_corn ? `<b>${game.score_tomato}</b>` : game.score_tomato;
            const topScorer = game.top_scorers ? `${game.top_scorers} (${game.top_goals})` : '—';
            const played = game.player_played ? `✅${game.player_squad_emoji ? ' ' + game.player_squad_emoji : ''}` : '—';
            html += `<tr${game.player_played ? ' class="player-played"' : ''}>
                <td class="date-col">${game.date}</td>
                <td class="team-col">🌽</td>
                <td class="score-col">${cornScore}&nbsp;:&nbsp;${tomatoScore}</td>
                <td class="team-col">🍅</td>
                <td>${topScorer}</td>
                <td class="played-col">${played}</td>
            </tr>`;
        });
        html += '</tbody></table></div>';
        content.innerHTML = html;
    } catch (error) {
        console.error('Error loading games log:', error);
        content.innerHTML = '<div class="error">Ошибка при загрузке истории игр</div>';
    }
}

async function loadAlltimeStatsTable() {
    try {
        const response = await fetch('/api/alltime-stats');
        const data = await response.json();
        if (data.success) {
            // Header
            document.getElementById('alltime-stats-header').textContent =
                `Всего игр сыграно: ${data.stats_goals_games[0]}. Всего голов забито: ${data.stats_goals_games[1]}. Всего автоголов забито: ${data.stats_goals_games[2]}`;

            // Table
            const content = document.getElementById('alltime-stats-content');
            let html = `<div class="table-responsive"><table class="stat-table"><thead><tr>
                <th>N</th><th>Игрок</th><th>Игры</th><th>Голы</th><th>Асисты</th><th>Автоголы</th><th>Гол/Игра</th><th>Побед</th><th>% Побед</th>
            </tr></thead><tbody>`;
            data.stats.forEach((player, i) => {
                html += `<tr>
                    <td>${i+1}</td>
                    <td>${player.first_name} ${player.last_name}</td>
                    <td>${player.games_played}</td>
                    <td>${player.goals}</td>
                    <td>${player.assists}</td>
                    <td>${player.own_goals}</td>
                    <td>${player.avg_goals}</td>
                    <td>${player.wins}</td>
                    <td>${player.win_rate}%</td>
                </tr>`;
            });
            html += '</tbody></table></div>';
            content.innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading alltime stats:', error);
        document.getElementById('alltime-stats-content').innerHTML = '<div class="error">Ошибка при загрузке статистики</div>';
    }
}