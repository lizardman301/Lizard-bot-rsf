const { SlashCommandBuilder, Embed } = require('@discordjs/builders');
const cachios = require('cachios');
const { bold } = require('../utilities/utilities');

const cache_days = 28;
/*
const cached_glossary = setup({
	// `axios` options
	url: 'https://glossary.infil.net/json',

	// `axios-cache-adapter` options
	cache: {
		maxAge: cache_days * 24 * 60 * 60 * 1000,
	},
});
*/

// https://stackoverflow.com/questions/15033196/using-javascript-to-check-whether-a-string-contains-japanese-characters-includi
function containsJapanese(s) {
	return /[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]/g.test(s);
}
function stripPuncAndSpace(s) {
	// eslint-disable-next-line no-useless-escape
	return s.replace(/[.,\/#!$%\^&\*;:{}=\-_`~() '"]/g, '').replace(/\s{2,}/g, ' ');
}

function searchForTerm(termString, terms) {
	const s = stripPuncAndSpace(termString.toLowerCase());

	const altMatches = {};

	let regex;
	try {
		regex = new RegExp(s, 'i');
	}
	catch (err) {
		console.log('error with glossary search:', err);
		// badly formed search query, just abandon ship
		return;
	}

	// search in terms and in definitions separately
	let inTerm = [];
	const inDef = [];
	for (const t in terms) {
		let found = false;
		let bestMatch = null;
		for (let i = 0; i < terms[t].termStripped.length; i++) {
			if (terms[t].termStripped[i].match(regex)) {
				found = true;

				// find out how close of a match it is based on # of letters in search term vs matching term
				const diff = terms[t].termStripped[i].length - s.length;
				// save this difference in the array (for now), so we can sort based on it
				// we don't know if this is our closest match yet, so keep track of our best match
				if (bestMatch === null || bestMatch[1] > diff) {
					bestMatch = [terms[t], diff];
					// this matched a secondary term, so save it in "altMatches" so we can display it later
					if (i > 0) {
						altMatches[terms[t].term] = terms[t].altterm[i - 1];
					}
				}
			}
		}
		if (bestMatch) {
			inTerm.push(bestMatch);
		}
		// if not found in a term and length of search query is 3 or more letters, search in definition
		if (!found && (s.length > 2 || containsJapanese(s)) && terms[t].defStripped.match(regex)) {
			inDef.push(terms[t]);
		}
	}

	function alpha(a, b) { return a.term.localeCompare(b.term); }

	// sort by closeness first, then alpha
	inTerm.sort((a, b) => a[1] - b[1] || alpha(a[0], b[0]));

	// flatten the array now that we've sorted based on closeness
	inTerm = inTerm.map(a => a[0]);
	inDef.sort(alpha);

	// concatenate all the sorted arrays
	inTerm.push.apply(inTerm, inDef);

	return inTerm;
}

async function prepareData() {
	const terms = {};
	const res = await cachios.get('https://glossary.infil.net/json/glossary.json', { ttl: cache_days * 24 * 60 * 60 });
	const data = res.data;

	data.forEach(function(d) {
		if (d.term.length > 0) {
			terms[d.term.toLowerCase()] = d;
			d.termStripped = [stripPuncAndSpace(d.term)];
			if (Object.prototype.hasOwnProperty.call(d, 'altterm')) {
				for (const st of d.altterm) {
					d.termStripped.push(stripPuncAndSpace(st));
				}
			}
			// create a definition stripped of punc and space that can be searched
			// we can just append the JP text to this so it is also searchable, this is never shown on screen
			d.defStripped = stripPuncAndSpace(d.def) + (Object.prototype.hasOwnProperty.call(d, 'jp') ? stripPuncAndSpace(d.jp) : '');
		}
	});
	return terms;
}

// Changed from Infil's original to clear links to make Discord look better
function doLinkReplacement(str) {
	str = str.split('<br>')[0];

	// parse out the in-glossary links from the definition and assign them as actual working hyperlinks
	let sind = str.indexOf('!<');
	while (sind >= 0) {
		const eind = str.indexOf('>', sind);
		if (eind < 0) {
			// something bad happened and we didn't format the link properly
			break;
		}
		const def_list = str.substring(sind + 3, eind - 1).split(',');
		const s = def_list.slice(-1)[0].replace(/'/g, '');

		str = str.substring(0, sind) + s + str.substring(eind + 1);
		sind = str.indexOf('!<');
	}

	// parse out links to non-glossary pages
	sind = str.indexOf('?<');
	while (sind >= 0) {
		const eind = str.indexOf('>', sind);
		if (eind < 0) {
			// something bad happened and we didn't format the link properly
			break;
		}
		const def_list = str.substring(sind + 3, eind - 1).split(',');
		const s = def_list.slice(-1)[0].replace(/'/g, '');

		str = str.substring(0, sind) + s + str.substring(eind + 1);
		sind = str.indexOf('?<');
	}

	return str;
}

module.exports = {
	data: new SlashCommandBuilder()
		.setName('glossary')
		.setDescription('No Description at the moment')
		.addStringOption(option => option.setName('term').setDescription('Use a term to help search the glossary'))
		.addBooleanOption(option => option.setName('video').setDescription('Set to True to add an example gif to the term (if available)')),
	async execute(interaction) {
		const base_url = 'https://glossary.infil.net/';
		const term = interaction.options.getString('term');

		if (!term) {
			await interaction.reply(base_url);
			return;
		}
		await interaction.deferReply();
		const infil_glossary = await prepareData();
		const searched_terms = searchForTerm(term, infil_glossary);

		if (searched_terms) {
			await interaction.editReply(bold(searched_terms[0].term) + ': ' + doLinkReplacement(searched_terms[0].def, infil_glossary));
		}
		else {
			await interaction.editReply('Term not found');
		}

		// Everything here is basically what is left from a 1:1 translation from the python version but it doesn't work
		// First Embed attempt (searched_terms === 1) is closer to the discord.js implementation
		// ---------------------------------------
		/*
		// This gets the True/False flag for a video clip
		const videoFlag = interaction.options.getBoolean('video');

		const sender = interaction.user;
		const number_emojis = { '1': '1⃣', '2': '2⃣', '3': '3⃣', '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣', '8': '8⃣', '9': '9⃣', '0': '0⃣' };

		const user_term = term.split(' ').join('%20');

		const st_dict = {};
		for (let x = 1; x <= searched_terms.length; x++) {
			st_dict[x] = searched_terms[x - 1];
		}

		if (searched_terms.length == 1) {
			infil_glossary.forEach(async glos_term => {
				if (glos_term['term'] == st_dict[1][0]) {
					const def_embed = new Embed()
						.setColor('0fa1dc')
						.setTitle(bold(term['term']))
						.setURL(`${base_url}?t=${user_term}`)
						.addFields(
							{ name: 'Definition', value: doLinkReplacement(term['def']), inline: true },
							{ name: '\u200B', value: '\u200B' },
							{ name: 'Link', value: `[Glossary Page For Term](${base_url}?t=${user_term}})`, inline: false },
						);

					await interaction.channel.send({ embeds: [def_embed] });

					try {
						if (videoFlag) {
							return 'https://gfycat.com/{0}'.format(term['video'][0]);
						}
					}
					catch (err) {
						return 'No video available';
					}
				}
			});
		}
		else if (searched_terms.length > 1) {
			const pick_embed = new Embed().setTitle('').setColor('0fa1dc');
			pick_embed.setFooter('Which term did you mean?');
			for (let x = 1; x <= searched_terms.length; x++) {
				pick_embed.addField(x, searched_terms[x - 1][0]);
			}

			let pick_msg;
			try {
				pick_msg = await interaction.channel.send({ embeds: [pick_embed] });
			}
			catch (err) {
				throw bold('Glossary') + ': Error sending embed to chat. Give Lizard-BOT the permission: ' + bold('Embed Links');
			}

			for (let x = 1; x <= searched_terms.length; x++) {
				await pick_msg.react(number_emojis[String(x)]);
			}

			const filter = (reaction, user) => {
				return Object.values(number_emojis).includes(reaction.emoji.name) && user.id === sender.id;
			};

			pick_msg.awaitReactions({ filter, max: 1, time: 60000, errors: ['time'] })
				.then(async collected => {
					const reaction = collected.first();

					for (const [key, value] of Object.entries(number_emojis)) {
						if (value === reaction.emoji.name) {
							for (const glos_term in infil_glossary) {
								if (infil_glossary[glos_term]['term'] === st_dict[parseInt(key)][0]) {
									await pick_msg.delete();

									const def_embed = new Embed()
										.setColor('0fa1dc')
										.setTitle(bold(infil_glossary[glos_term]['term']))
										.setURL(`${base_url}?t=${user_term}`)
										.addFields(
											{ name: 'Definition', value: doLinkReplacement(infil_glossary[glos_term]['def']), inline: true },
											{ name: '\u200B', value: '\u200B' },
											{ name: 'Link', value: `[Glossary Page For Term](${base_url}?t=${user_term}})`, inline: false },
										);

									await interaction.channel.send({ embeds: [def_embed] });

									try {
										if (videoFlag) {
											return 'https://gfycat.com/{0}'.format(infil_glossary[glos_term]['video'][0]);
										}
									}
									catch (err) {
										return 'No video available';
									}
								}
							}
						}
					}
				})
				.catch(async function() {
					await pick_msg.reply(bold('Glossary') + ': Issue with the terms');
				});


			let user_to_check;
			let msg_to_check;
			let reaction_read_emoji;
			while (!(user_to_check == sender) || !(msg_to_check == pick_msg) || !(Object.values(number_emojis).includes(reaction_read_emoji))){
				try {
					reaction_read, user_to_check  = await client.wait_for('reaction_add', timeout=60.0)
					msg_to_check = reaction_read.message
					if (msg_to_check == pick_msg && user_to_check == sender):
						reaction_read_emoji = reaction_read.emoji
						if reaction_read_emoji in number_emojis.values():
							for key,value in number_emojis.items():
								if value == reaction_read_emoji:
									for term in infil_glossary:
										if term['term'] == st_dict[int(key)][0]:
											await pick_msg.delete()
											def_embed = Embed(title=bold(term['term']), colour=Colour(0x0fa1dc))
											def_embed.add_field(name="Definition", value=fix_link_regex(term['def']))
											def_embed.add_field(name="Link", value="[Glossary Page For Term]({}?t={})".format(base_url, user_term), inline=False)
											await channel.send(embed=def_embed)
											try:
												if(videoFlag):
													return "https://gfycat.com/{0}".format(term['video'][0])
												return
											except:
												#no video,
												return "No video available"
				}
				catch (err) {
					await pick_msg.delete()
					raise Exception(bold("Glossary") + ": Issue with the terms")
				}
			}
		}
		else {
			await interaction.reply(bold('Glossary') + ': No terms found');
		}
		*/
	},
};