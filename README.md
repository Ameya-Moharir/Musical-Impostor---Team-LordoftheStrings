<h1>Musical Impostor</h1>
<h2>Musical Version of Among Us</h2>
 <h1>Musical Impostor 🎵🎭</h1>

   <p><strong>Musical Impostor</strong> is a musical twist on the popular social deduction game <em>Among Us</em>. In this game, 4 to 10 players join a room and listen to a song from a shared playlist. However, one player, the "Impostor," hears a different song from another playlist. After a 30-second listening round, players engage in a discussion to identify the Impostor. Afterward, they vote on who they think the Impostor is. If the Impostor is voted out, the game ends. If the Impostor survives, the players lose.</p>

   <p>To add more suspense, before the listening round begins, the Impostor can sabotage one player by making them hear the same incorrect song as the Impostor.</p>

   <h2>Game Mechanics</h2>
    <ul>
        <li><strong>Player Count:</strong> 4 to 10 players join a room.</li>
        <li><strong>Playlist:</strong> All players (except the Impostor) hear the same song from a playlist that fits the selected theme.</li>
        <li><strong>Impostor's Role:</strong> The Impostor listens to a different song from another playlist and can sabotage another player.</li>
        <li><strong>Discussion & Voting:</strong> 
            <ul>
                <li>After a 30-second listening round, players discuss for 100 seconds to find out who the Impostor is.</li>
                <li>Voting follows, and if the Impostor is voted out, the players win. If not, the Impostor wins.</li>
            </ul>
        </li>
    </ul>

   <h2>Technologies Used</h2>
    <ul>
        <li><strong>Backend:</strong> Flask</li>
        <li><strong>Frontend:</strong> HTML, CSS, JavaScript</li>
        <li><strong>Real-time Functionality:</strong> WebSockets for room creation and music synchronization</li>
    </ul>

  <h2>Project Status</h2>
    <p>This project is a work in progress. As a team new to these technologies, we encountered challenges, particularly with WebSockets for synchronizing music and event handling, which led to an incomplete implementation. Specifically, issues with real-time event management and debugging prevented us from completing the full functionality.</p>

   <h2>Setup Instructions</h2>
    <p>To set up the project, follow these steps:</p>
    <ol>
        <li>Clone the repository:
            <pre><code>git clone https://github.com/your-repo/musical-impostor.git
cd musical-impostor</code></pre>
        </li>
        <li>Install dependencies:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Run the Flask app:
            <pre><code>python app.py</code></pre>
        </li>
        <li>After running the app, a global link will be generated in the console.</li>
        <li>Open the link in your browser to access the homepage.</li>
        <li>From the homepage, you can either:
            <ul>
                <li><strong>Create a Room:</strong> Set the maximum number of players and enter your nickname. A room ID will be generated for you to share with friends.</li>
                <li><strong>Join a Room:</strong> Enter your nickname and the room ID shared by the host.</li>
            </ul>
        </li>
        <li>Once all players have joined, the host can start the game.</li>
        <li>During the game:
            <ul>
                <li>After the 30-second listening round, you will go to a discussion page where you can discuss with other players for 100 seconds.</li>
                <li>After the discussion, you will enter the voting round to vote out the suspected Impostor.</li>
            </ul>
        </li>
    </ol>

   <h2>Known Issues</h2>
    <ul>
        <li><strong>WebSocket Synchronization:</strong> We faced challenges in synchronizing the music playback across all clients using WebSockets.</li>
        <li><strong>Event Handling:</strong> Debugging event-handling issues proved complex, and we were unable to fully resolve them within the project timeline.</li>
    </ul>

  <p>We hope to resolve these issues in future versions and improve the overall experience.</p>
</body>
</html>
