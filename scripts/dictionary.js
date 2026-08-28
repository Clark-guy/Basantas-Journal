
//This is a utility script to be used with node.js

//I have a JSON dictionary of nepali words.
//First thing I want to do is loop through all the words and add a blank "devanagari" key

import { writeFile, readFile } from 'fs/promises';
import { translate } from 'google-translate-api-x';

async function loadWOTD(filepath){
    try {
        const rawData = await readFile(filepath, 'utf8');
        const data = JSON.parse(rawData);
        for (const word of data){
            try {
                const res = await translate(word.english, { to: 'ne' });
                /*console.log(word.english);
                console.log(res.text);
                console.log(res.raw[0]);*/
                word.devanagari = res.text;
                //TODO find out how to grab the latin character form of the word for pronunciation
            }
            catch (error){
                throw new Error(`failed to translate word ${error}`)
            }
            console.log(word.english);
        }
        console.log(data);
        const outputString = JSON.stringify(data, null, ' ')
        await writeFile(filepath, outputString, 'utf8');

    }
    catch (error){
        throw new Error(`WOTD failed to load. ${error}`)
    }
};

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