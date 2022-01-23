const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageActionRow, MessageButton, ButtonInteraction, MessageEmbed } = require('discord.js');
const { waitForDebugger } = require('inspector');
const utilities = require('util');
const raw_rs = require('../utilities/rs.json');
const { get_randomselect_data } = require('../utilities/utilities');

const init_games = Object.keys(Object.values(raw_rs)[0]).filter(function(obj) { return Object.keys(Object.values(raw_rs)[1]).indexOf(obj) >= -1; });

const types = [];
const supported_games = [];

Object.keys(raw_rs).forEach(type => {
	types.push([type, type]);
});

init_games.forEach(game => {
    if (raw_rs['character'][game].length - 1 >= 7) {
        supported_games.push([game, game]);
    }
});

module.exports = {
	data: new SlashCommandBuilder()
		.setName('draw')
		.setDescription('Draws 7 random characters and conducts a ban pick system. SFV characters if no game specified.')
        .addUserOption(option => option.setName('player').setDescription('user to challenge').setRequired(true))
        .addStringOption(option => option.setName('game').setDescription('Choose a game (defaults to SFV if not specified)').addChoices(supported_games)),
	async execute(interaction) {
        const NUM_CHARS = 7;
        const game = interaction.options.getString('game');
        let data, games;
        try {
            let rsGame = game !== null ? game : 'sfv';
            [data, games] = get_randomselect_data(rsGame, 'character');
        } catch (err) {
            console.log(err);
        }
        let player1 = interaction.member;
        let player2 = interaction.options.getMember('player');
        if ( player1.id === player2.id ) {
            await interaction.reply({ content: 'You cannot challenge yourself to draw.', ephemeral: true });
        } else {
        const row = new MessageActionRow()
            .addComponents(
                new MessageButton()
                    .setCustomId('yes')
                    .setLabel('Yes')
                    .setStyle('SUCCESS'),
                new MessageButton()
                    .setCustomId('no')
                    .setLabel('No')
                    .setStyle('DANGER')
            );
        const message = await interaction.reply({
            content: 'Do you agree to draw <@' + player2.id + '>',
            components: [row],
            fetchReply: true
        });

        const collector = message.createMessageComponentCollector({time: 1000 * 5});

        let accepted = false;
        const rsRow1 = new MessageActionRow();
        const rsRow2 = new MessageActionRow();
        
        let rsChars = [];        
        for(let i = 0; i < NUM_CHARS; i++) {
            let rsChar = data[Math.floor(Math.random() * data.length)];
            // prevent adding more than 1 of the same character
            while(rsChars.filter(character => character === rsChar).length > 0) {
                chosen = data[Math.floor(Math.random() * data.length)];
            }
            rsChars.push(rsChar);
        }
        
        for(let i = 0; i < rsChars.length; i++) {
            // 4 rows on top, 3 rows on bottom
            if (i <= 3) {
                rsRow1.addComponents(
                    new MessageButton()
                        .setCustomId('' + rsChars[i])
                        .setLabel('' + rsChars[i])
                        .setStyle('SUCCESS')
                );
            } else {
                rsRow2.addComponents(
                    new MessageButton()
                        .setCustomId('' + rsChars[i])
                        .setLabel('' + rsChars[i])
                        .setStyle('SUCCESS')
                );
            }
        }

        // randomly choose player order
        let playerOrder = [[player1,player2,player1,player2,player2,player1],[player2,player1,player2,player1,player1,player2]][Math.floor(Math.random() * 2)];
        let currTurn = 0;
        let embed = new MessageEmbed()
            .setColor('#0fa1dc')
            .setTitle('Card Draw')
            .setFooter({text: playerOrder[currTurn].displayName + ', select a character to ban.'});
        let p1Chars = [];
        let p2Chars = [];
        let rowToUse;
        let charButton;
        collector.on('collect', async (btnInt) => {
            await btnInt.deferUpdate();
            if ( btnInt.user.id !== player1.id && btnInt.user.id !== player2.id ) {
                btnInt.reply({content: 'You are not the challenged user.', ephemeral: true});
            } else if ( !accepted ) {
                if ( btnInt.user.id === player2.id) {
                    if ( btnInt.customId === 'yes' ) {
                        accepted = true;
                        await btnInt.editReply({embeds: [embed], components: [rsRow1, rsRow2]});
                        collector.resetTimer();  
                    } else {
                        // draw is declined. message is in end collection
                        collector.stop();
                    }
                } else {
                    btnInt.reply({content: 'You are not the challenged user.', ephemeral: true});
                }
            } else if ( playerOrder[currTurn].id === btnInt.user.id ) {
                // challenge is accepted
                rowToUse = rsRow1.components.filter(btn => btn.customId === btnInt.customId).length > 0 ? rsRow1 : rsRow2;
                // get the selected character button and disable it
                charButton = rowToUse.components.find(btn => btn.customId === btnInt.customId);
                charButton.setDisabled(true);

                
                if ( currTurn >= 2) {
                    if ( playerOrder[currTurn] === player1 ) {
                        p1Chars.push(charButton.customId);
                    } else {
                        p2Chars.push(charButton.customId);
                    }
               }
                currTurn++;
                // p1ban, p2ban, p1pick, p2pick, p2pick, p1pick
                // p2ban, p1ban, p2pick, p1pick, p1pick, p2pick
                if ( currTurn < playerOrder.length ) {
                    if ( currTurn < 2 ) { // ban phase
                        embed = new MessageEmbed(message.embeds[0])
                        .setColor('#0fa1dc')
                        .setTitle('Card Draw')
                        .setFooter({text: playerOrder[currTurn].displayName + ', select a character to ban.'});
                    }  else if ( currTurn === 4 ) { // second player picks twice
                        embed = new MessageEmbed(message.embeds[0])
                        .setColor('#0fa1dc')
                        .setTitle('Card Draw')
                        .setFields(
                            {name: player1.displayName, value: '\u200b' + p1Chars, inline: true},
                            {name: player2.displayName, value: '\u200b' + p2Chars, inline: true}
                            )
                        .setFooter({text: playerOrder[currTurn].displayName + ', select another character to pick.'});
                    } else { // all other phases
                        embed = new MessageEmbed(message.embeds[0])
                        .setColor('#0fa1dc')
                        .setTitle('Card Draw')
                        .setFields(
                            {name: player1.displayName, value: '\u200b' + p1Chars, inline: true},
                            {name: player2.displayName, value: '\u200b' + p2Chars, inline: true}
                            )
                        .setFooter({text: playerOrder[currTurn].displayName + ', select a character to pick.'});
                    }
                    await btnInt.editReply({embeds: [embed], components: [rsRow1, rsRow2]});
                    collector.resetTimer();
                } else {
                    collector.stop();
                }
            }
            });
            

            collector.on('end', async (collection) => {
                try {
                    await message.delete(); // delete the initial challenge
                    if (!accepted) {
                        interaction.followUp({content: 'The draw was not accepted.', ephemeral: true});
                    } else if ( p1Chars.length < 2 || p2Chars < 2 ) {
                        interaction.followUp({content: 'The draw was not completed in time.', ephemeral: true});
                    } else {
                        embed = new MessageEmbed()
                                .setColor('#0fa1dc')
                                .setTitle('Card Draw Finished')
                                .setFields(
                                    {name: player1.displayName, value: '\u200b' + p1Chars, inline: true},
                                    {name: player2.displayName, value: '\u200b' + p2Chars, inline: true}
                                );
                        interaction.followUp({embeds: [embed]});
                    }
                } catch(e) {
                    // someone deleted the initial challenge before everything was finished
                    console.log(e.stack);
                }
            });
        }
	},
};