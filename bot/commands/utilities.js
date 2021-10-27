function bold(string) {
	return '**' + string + '**';
}

function get_chal_tour_id(bracket_msg) {
	// designed to return the tournament identifier if it exists in the database bracket text
	// returns empty string otherwise

	// regex for <community_url>.challonge.com/<tournament identifier> or challonge.com/<tournament identifier>
	const regex = new RegExp('[-a-zA-Z0-9@:%._+~#=]{0,256}.challonge.com/[a-zA-Z0-9_]+');
	let url = '';
	let tour_id = '';

	// find first match and make that the url to work off of
	// if no match, return empty string immediately
	const matches = regex.exec(bracket_msg);
	if (matches !== null) {
		url = matches[0];
	}
	else {
		throw 'No bracket link set';
	}

	// get the identifer from the back part of the url
	// should only be one slash so we split on that
	// get the last group in order to get the tournament identifier
	tour_id = url.split('/').pop();
	return tour_id;
}

function get_randomselect_data(game, random_type='character'){ 
    const rs_info = require('./bot/commands/rs.json');
    let games = Object.keys(rs_info[random_type]);

    if(!games.includes(game)){
        return [], games
    }
    let values = Object.values(rs_info[random_type][game]);
    return values.splice(0, values.length - 1), games
}

// Get all users in a Discord
function get_users(users) {
	const userDict = {};

	// Get their distinct name and their nickname
	users.forEach(user => {
		userDict[user['name'] + '#' + String(user['discriminator'])] = [user['display_name'].toLowerCase(), user['mention']];
	});

	return userDict;
}

// Perform regex to find out if a string is a Discord channel
function is_channel(channel) {
	const regex = new RegExp('<#[0-9]*>');
	if (channel.match(regex)) {
		return BigInt(channel.slice(2, -1));
		// Return only the channel ID
	}
	return 0;
}

// Simplify removing pings more
function pings_b_gone(mentions) {
	let mention_list = {};
	// Empty dict to store values in

	// For each mention, get the name and the mention value
	mentions.forEach(mention => {
		let ping = '<@!' + String(mention.id) + '>';
		if (mention.nick) {
			mention_list[mention.nick] = ping;
			return;
		}
		mention_list[mention.name] = ping;
	});

	return mention_list;
}

function checkin(parts, users) {
	// Discord server usernames and mentions
	users = Object.values(users);
	// Used for people missing from the server
	const not_discord_parts = [];
	// Used for people not checked in
	const not_checked_in_parts = [];
	// Discord server usernames
	const usernames = [];
	// Discord server mentions
	const mentions = [];

	users.forEach(user => {
		const userValues = Object.values(user)[0];
		usernames.push(userValues[0]);
		mentions.push(userValues[1]);
	});

	// Check each participant to see if they are in the server and checked in
	parts.forEach(p => {
		p = p['participant'];

		const name_lower = p['display_name'].toLowerCase();
		const name_escaped = Util.escapeMarkdown(p['display_name']);
		const challonge_name_lower = p['challonge_username'] ? p['challonge_username'].toLowerCase() : name_lower;

		if (!p['checked_in']) {
			not_checked_in_parts.push(name_escaped);
		}

		if (!(usernames.find(elem => { return elem.toLowerCase().includes(name_lower); })) && !( usernames.find(elem => { return elem.toLowerCase().includes(challonge_name_lower); }))) {
			not_discord_parts.push(name_escaped);
		}

		if ((!(not_discord_parts.includes(name_escaped)) && (not_checked_in_parts.includes(name_escaped))) && ((usernames.find(elem => { return elem.toLowerCase().includes(name_lower); })) || (usernames.find(elem => { return elem.toLowerCase().includes(challonge_name_lower); })))) {
			const match = usernames.filter(elem => { elem = elem.toLowerCase(); if (elem.includes(name_lower) || elem.includes(challonge_name_lower)) { return true; } else { return false; } });

			not_checked_in_parts[not_checked_in_parts.indexOf(name_escaped)] = mentions[usernames.indexOf(match[0])];
		}
	});

	not_checked_in_parts.sort();
	not_discord_parts.sort();

	return [not_checked_in_parts, not_discord_parts];
}

function seeding(sheet_id, parts, url, seed_num) {
    player_points = [] // Stores "player point_value" for sorting later

    // Get dict of associated players and their points
    players_to_points = sheets(sheet_id)

    // Check each participant and if they have points
    for p in parts:
        p = p['participant']

        // If player has points and is active (checked in), add to list for later sorting
        if (p['challonge_username'] in players_to_points) and p['checked_in']:
            player_points.append(p['challonge_username'] + ' ' + players_to_points[p['challonge_username']])

    /*
	Players are listed by highest points and then alphabetically
    Truncated by how many we are seeding
    First sort is done on the player name, players with names higher in the alphabet win ties
    Second sort is done on the point value
	*/
    player_points = sorted(sorted(player_points, key=lambda part: part.split(' ')[0].lower()), key=lambda part: int(part.split(' ')[1]), reverse=True)[0:seed_num if 0 < seed_num <= len(player_points) else len(player_points)]

    // Associate seeding number with the player
    finished_seeding ={}
    for x in range(len(player_points)):
        finished_seeding.update({x+1: player_points[x]})

    // Randomize the seeding to ensure a fairer bracket
    response = requests_post(url + "/participants/randomize.json", headers={"User-Agent":"Lizard-BOT"}, auth=(chal_user, api_key))
    if '401' in str(response.status_code):
        raise Exception(bold("Challonge") + ": Lizard-BOT does not have access to that tournament")
    elif '200' not in str(response.status_code):
        print(response.text)
        raise Exception(bold("Challonge") + "Unknown Challonge error for <" + url + "> while randomizing seeds")

    // Check if player is in sorted, truncated list and update their seed number
    for player in finished_seeding:
        for p in parts:
            p = p['participant']

            // If Challonge user equals the username we have for seeding
            // Then, update seed number with their index location
            if p['challonge_username'] == finished_seeding[player].split(' ')[0]:
                response = requests_put(url + "/participants/" + str(p['id']) + ".json", headers={"User-Agent":"Lizard-BOT"}, auth=(chal_user, api_key), params={'participant[seed]':player})
                if '200' in str(response.status_code):
                    continue
                elif '401' in str(response.status_code):
                    raise Exception(bold("Challonge") + ": Lizard-BOT does not have access to that tournament")
                else:
                    print(response.text)
                    raise Exception(bold("Challonge") + "Unknown Challonge error for <" + url + "> while seeding: " + player)

    // Return seeding list
    return finished_seeding
}

// Read a stat from database for a given command
function read_stat(command, func_map) {
    stats = {}
    conn = make_conn() // Make DB Connection

    try:
        with conn.cursor() as cursor:
            // Update the desired setting in the DB for the given guild/channel
            if command:
                if 'challonge' in command or 'edit' in command:
                    function = command.split('_')[0]
                else:
                    function = func_map[command].__name__

                sql = "SELECT command, used FROM stats WHERE command = %s"
                cursor.execute(sql, (function))
            else:
                sql = "SELECT command, used FROM stats"
                cursor.execute(sql)
            for row in cursor:
                row_command = row['command']
                if row_command in ['ping']:
                    row_command = 'lizardman'
                elif row_command in ['round_lizard']:
                    row_command = 'round'
                elif row_command in ['prefix']:
                    row_command = 'prefix-lizard'
                elif row_command in ['stats']:
                    row['used'] += 1
                stats.update({row_command.replace('_', '-'):row['used']})
    finally:
        conn.close() // Close the connection

    return stats
}

// Increment a command usage in the database
function stat_up(command) {
    if 'challonge' in command or 'edit' in command:
        command = command.split('_')[0]

    conn = make_conn() // Make DB Connection

    try:
        with conn.cursor() as cursor:
            // Check to see if the command already has been used
            sql = "SELECT used FROM stats WHERE command = %s"
            cursor.execute(sql, (command))
            result = cursor.fetchone()

            // Check the result for how many times a command was used
            if result:
                // Add another use for an existing command
                sql = "UPDATE stats SET used = %s WHERE command = %s"
                cursor.execute(sql, (result['used']+1,command))
            else:
                // Add a command into the database
                sql = "INSERT INTO stats (command) VALUES (%s)"
                cursor.execute(sql, (command))
    finally:
        conn.close() // Close the connection
}

function read_disable(server) {
    // Get setting from DB
    disabled_list = []
    conn = make_conn() // Make DB Connection

    try:
        with conn.cursor() as cursor:
            // Select the disabled list for the server from the table
            // Return as a python list
            sql = "SELECT `disabled_list` FROM guild_settings WHERE guild_id = %s"
            cursor.execute(sql, (server))
            disabled_list=json_loads(cursor.fetchone()['disabled_list']) // Return the value for the setting
    finally:
        conn.close() // Close the connection

    return disabled_list
}

function set_disable(server, command) {
    // List of commands you cannot disable
    dont_disable =["disable","edit","enable","prefix"]

    if command.split('_')[0] in dont_disable:
        // Command is one that is not allowed to be disabled
        raise Exception("Cannot disable important command.")

    // Get current disable list first
    disabled_list = read_disable(server)

    if command in disabled_list:
        // Already disabled, return error
        raise Exception("Command already disabled.")

    // Add new command
    disabled_list.append(command)
    // Sort alphabetically
    disabled_list = sorted(disabled_list)

    // Set new list in db
    conn = make_conn() // Make DB Connection

    try:
        with conn.cursor() as cursor:
            // Update the table with the new disabled list as a json dump
            sql = "UPDATE guild_settings SET disabled_list = %s WHERE guild_id = %s"
            cursor.execute(sql, (json_dumps(disabled_list),server))
    except:
        // Something went completely wrong here if a new row wasn't created in disabled_list
        raise Exception("Could not save list to table")
    finally:
        conn.close() // Close the connection

    return disabled_list // in case you need it.
}

function set_enable(server, command) {
    // Get current disable list first
    disabled_list = read_disable(server)
    if not disabled_list:
        // List is empty
        raise Exception("There is nothing disabled.")
    elif command not in disabled_list:
        // Already disabled, return error
        raise Exception("Command is not disabled.")

    // Remove command
    disabled_list.remove(command)

    // Set new list in db
    conn = make_conn() // Make DB Connection

    try:
        with conn.cursor() as cursor:
            // Update the table with the new disabled list as a json dump
            sql = "UPDATE guild_settings SET disabled_list = %s WHERE guild_id = %s"
            cursor.execute(sql, (json_dumps(disabled_list),server))
    except:
        // Something went completely wrong here if a new row wasn't created in disabled_list
        raise Exception("Could not save list to table")
    finally:
        conn.close() // Close the connection

    return disabled_list // in case you need it.
}