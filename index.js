/* TODO: 
** Drop points 
** Ordnance
** Heirloom weapon check [DONE]
** Special map interactions: I.E: Charge Tower (KC), Trials Challenge/Open Vaults (WE), MRVN (Olympus), Prowler's Den (SP)
** Check map function [DONE] [TODO: Lessen API usage]
** Roulette function [DONE]
** Better API inclusion [DONE]
*/

const fetch = require("node-fetch")
const secrets = require('./secrets.json' );
const alert = require('alert');
const fs = require('fs');
const rawData = JSON.parse(fs.readFileSync('./data2.json', 'utf8'));
const mapData = JSON.parse(fs.readFileSync('./mapData.json', 'utf8'));

let mozambiqueApiMap = `https://api.mozambiquehe.re/maprotation?version=2&auth=${secrets.authtoken}`

var LEGENDS = ["Bloodhound", "Gibraltar", "Lifeline", "Pathfinder", "Wraith", "Bangalore", "Caustic", "Mirage", "Octane", "Wattson", "Crypto", "Revenant", "Loba", "Rampart", "Horizon", "Fuse", "Valkyrie", "Seer", "Ash", "Mad Maggie", "Newcastle"];

var timedWeapon = false;
var pL = ["","",""];
var pWP = ["","",""];
var pWS = ["","",""];
var cMap;
var heirloomreplacement;

// Required
function request(self, url) {
    return fetch(url, {
      headers: self.headers,
    })
    .then(function (res) {
      return res.json();
    })
    .catch(function (err) {
      return Promise.reject(err);
    });
};
async function Initialize() {
    await mapCheck();
    pickLegends();
    pickWeapons();
    checkHeirloomWeaponTimedWeapon(pWP,pWS)
    //dropPoint(cMap); (Yet to be implemented)
    //specialRule(); (Not implemented)
    //mapSpecific(currentMap); (Not implemented)
    //availableOrdnance(pL); (Not implemented)
    finalAlert();
    
}
function mapRotation() {
    return request(this, mozambiqueApiMap);
}

async function mapCheck() {

    await request(this, mozambiqueApiMap).then(function (data) {
        

        const brC = data.battle_royale.current;
        const brN = data.battle_royale.next;
        endTime = brC.end;
        currentMap = brC.map;
        nextMap = brN.map;
        remainingSecs = brC.remainingSecs
        
        if (remainingSecs < 10) {
            cMap = nextMap;
            return cMap;
        }
        else {
            cMap = currentMap
            return cMap;
        }
    })
};

function pickLegends() {
    var legendArray = LEGENDS;
    for (let i = 0; i < pL.length; i++) {
        // Picks a random number for later use instead of directly getting a random number on the go
        let randomNum = Math.floor(Math.random()*legendArray.length)
        pL[i] = legendArray[randomNum];
        // Deletes array spot of picked legend in order to avoid duplicate legends (e.g. Gibraltar Gibraltar Valkyrie)
        legendArray.splice(randomNum, 1)
        }
}

async function pickWeapons() {
    for (let i = 0; i < pWP.length ; i++) {
        let weaponsCount = 28;
        randomNumP = Math.floor(Math.random() * (weaponsCount - 0) + 0)
        randomNumS = Math.floor(Math.random() * (weaponsCount - 0) + 0)

        weaponFinderP = rawData[0][randomNumP];
        weaponFinderS = rawData[0][randomNumS];
        
        weaponNameP = weaponFinderP.name;
        weaponRarityP = weaponFinderP.rarity;
        weaponTypeP = weaponFinderP.type;
        weaponAmmoTypeP = weaponFinderP.ammoType;

        weaponNameS = weaponFinderS.name;
        weaponRarityS = weaponFinderS.rarity;
        weaponTypeS = weaponFinderS.type;
        weaponAmmoTypeS = weaponFinderS.ammoType;

        if (randomNumP === 8) {
            PisCarSMG = true;
        } else {
            PisCarSMG = false;
        }
        if (PisCarSMG == true) {
            if ((Math.random() < 0.5) == true) {
            weaponAmmoTypeP = "CAR is in Light mode only"
            } else {
            weaponAmmoTypeP = "CAR is in Heavy mode only"
            }
        }
        if (randomNumS === 8) {
            SisCarSMG = true;
        } else {
            SisCarSMG = false;
        }
        if (SisCarSMG == true) {
            if ((Math.random() < 0.5) == true) {
            weaponAmmoTypeS = "CAR is in Light mode only"
            } else {
            weaponAmmoTypeS = "CAR is in Heavy mode only"
            }
        }
        pWP[i] = weaponFinderP;
        pWS[i] = weaponFinderS;
    }
}
function checkHeirloomWeaponTimedWeapon(pWP,pWS) {
    for (let i = 0; i < pWP.length; i++) {
        // Quick get rarity of weapon
        let pWPR = pWP[i].rarity;
        let pWSR = pWS[i].rarity;
        if (pWPR == "Heirloom" && pWSR == "Heirloom") {
            timedWeapon = true
            timedWeapons = ["RE-45", "P2020", "Wingman"];
            randomNum = Math.floor(Math.random() * (2 - 0) + 0)
            heirloomreplacement = `Care package replacement weapon for loadout ${i+1}: `+ timedWeapons[randomNum]
        }
    }
}
function finalAlert() {
   alert(
       `You're playing on ${cMap}!\n\n` +
       `Picked Legends: ${pL[0]}, ${pL[1]} and ${pL[2]}.`
        + `\n${pL[0]}   gets to use:     ${pWP[0].name}   and    ${pWS[0].name}.`
        + `\n${pL[1]}   gets to use:     ${pWP[1].name}   and    ${pWS[1].name}.`
        + `\n${pL[2]}   gets to use:     ${pWP[2].name}   and    ${pWS[2].name}.`
   ) 
    if (timedWeapon == true) {
        alert(heirloomreplacement)
    }
}


Initialize();