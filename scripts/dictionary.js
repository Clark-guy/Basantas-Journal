
//This is a utility script to be used with node.js. When run, it will take all
//english words in the ../wotd.json file and add on devanagari and romanized
//nepali. The format of the json file must already be correct for this to work.
//
//To run this script: run "node dictionary.js" from within the scripts folder.
//
//TODO:make a nicer way to input english words to save myself the trouble later
//e.g. if I could export an apple notes file and dump it in here...


import { writeFile, readFile } from 'fs/promises';
import { translate } from 'google-translate-api-x';
import { Sanscript } from '@indic-transliteration/sanscript'


async function loadWOTD(filepath){
    try {
        const rawData = await readFile(filepath, 'utf8');
        const data = JSON.parse(rawData);
        for (const word of data){
            if (!word.devanagari || !word.nepali) {
                try {
                    //console.log(word.english);
                    //console.log(res.text);
                    const res = await translate(word.english, { to: 'ne' });
                    word.devanagari = res.text;
                    word.nepali = Sanscript.t(res.text, 'devanagari', 'hk')
                    
                }
                catch (error){
                    throw new Error(`failed to translate word ${error}`)
                }
                console.log(word.english);
            }
        }
        const outputString = JSON.stringify(data, null, ' ')
        await writeFile(filepath, outputString, 'utf8');

    }
    catch (error){
        throw new Error(`WOTD failed to load. ${error}`)
    }
};

async function alphabetizeAndClearDupes(){
    try {
        const rawData = await readFile(filepath, 'utf8');
        const data = JSON.parse(rawData);
        // now sort the data here TODO
    }
    catch (error){
        throw new Error(`Failed to open file. ${error}`);
    }
}


loadWOTD("../wotd.json");

/*
at some point throw together a function to 
order WOTDs alphabetically. This will fuck
up the order for people's viewing but at that
time it could also be worth implementing some
randomization or even toying with hashing 
functions to pick the word, so it's not entirely
alphabetical (or even mostly, as it is now)
*/

/*
I forget how to run this. Just node dictionary.js maybe? Make a backup. */