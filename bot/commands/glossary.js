const { SlashCommandBuilder } = require('@discordjs/builders');
const cachios = require('cachios');
const { MessageEmbed } = require('discord.js');

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
		.setDescription('Searches https://glossary.infil.net/')
		.addStringOption(option => option.setName('term').setDescription('Use a term to help search the glossary').setRequired(true))
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

		if (searched_terms.length > 0) {
			const exampleEmbed = new MessageEmbed()
				.setColor('#0fa1dc')
				.setTitle(searched_terms[0].term)
				.setDescription(doLinkReplacement(searched_terms[0].def, infil_glossary)
			+ '\n\n[Glossary Page For Term](https://glossary.infil.net/?t=' + searched_terms[0].term + ')');
			await interaction.editReply({ embeds: [exampleEmbed] });
		}
		else {
			await interaction.editReply('Term not found');
		}
	},
};