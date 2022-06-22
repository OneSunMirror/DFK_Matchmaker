const search_opt = {
    "scoring_options" :  [
        { "name" : "Primary Class", "id" : 0},
        { "name" : "Sub Class", "id" : 1},
        { "name" : "Profession", "id" : 2},
        { "name" : "Passive 1", "id" : 3},
        { "name" : "Passive 2", "id" : 4},
        { "name" : "Active 1", "id" : 5},
        { "name" : "Active 2", "id" : 6} ],
    "index": [
        "Class",
        "Class",
        "Profession",
        "stats",
        "stats",
        "Skills",
        "Skills",
        "Skills",
        "Skills",
    ],
    "Class" : [
        { "name" : "Warrior", "id" : 0},
        { "name" : "Knight", "id" : 1},
        { "name" : "Thief", "id" : 2},
        { "name" : "Archer", "id" : 3},
        { "name" : "Priest", "id" : 4},
        { "name" : "Wizard", "id" : 5},
        { "name" : "Monk", "id" : 6},
        { "name" : "Pirate", "id" : 7},
        { "name" : "Berserker", "id" : 8},
        { "name" : "Seer", "id" : 9},
        { "name" : "Paladin", "id" : 16},
        { "name" : "DarkKnight", "id" : 17},
        { "name" : "Summoner", "id" : 18},
        { "name" : "Ninja", "id" : 19},
        { "name" : "Dargoon", "id" : 24},
        { "name" : "Sage", "id" : 25},
        { "name" : "Shapeshifter", "id" : 20},
        { "name" : "Dreadknight", "id" : 28}],
     "Profession"  :  [
        {"name" : "Mining", "id" :0 },
        {"name" : "Gardening", "id" :2 },
        {"name" : "Fishing", "id" :4 },
        {"name" : "Foraging", "id" :6 }],
    "Skills" :  [
        { "name" : "Basic1", "id" : 0},
        { "name" : "Basic2", "id" : 1},
        { "name" : "Basic3", "id" : 2},
        { "name" : "Basic4", "id" : 3},
        { "name" : "Basic5", "id" : 4},
        { "name" : "Basic6", "id" : 5},
        { "name" : "Basic7", "id" : 6},
        { "name" : "Basic8", "id" : 7},
        { "name" : "Basic9", "id" : 8},
        { "name" : "Basic10", "id" : 9},
        { "name" : "Advanced1", "id" : 16},
        { "name" : "Advanced2", "id" : 17},
        { "name" : "Advanced3", "id" : 18},
        { "name" : "Advanced4", "id" : 19},
        { "name" : "Elite1", "id" : 24},
        { "name" : "Elite2", "id" : 25},
        { "name" : "Advanced5", "id" : 20},
        { "name" : "Transcendant1", "id" : 28}],
    "Rarity" : [
        {"name" : "Common", "id" : 0},
        {"name" : "Uncommon", "id" : 1},
        {"name" : "Rare", "id" : 2},
        {"name" : "Legendary", "id" : 3},
        {"name" : "Mythic", "id" : 4}
    ],
    "Stats" : [
        {"name" : "Strength", "id" : 0},
        {"name" : "Agility", "id" : 2},
        {"name" : "Intelligence", "id" : 4},
        {"name" : "Wisdom", "id" : 6},
        {"name" : "Luck", "id" : 8},
        {"name" : "Vitality", "id" : 10},
        {"name" : "Edurance", "id" : 12},
        {"name" : "Dexterity", "id" : 14},
    ]
}
function create_drop_down(parent_id, name, id, options) {
    parent = document.getElementById(parent_id)
    code = '<strong>' + name + '</strong>'
    code =   code + '<div class="dropdown" id="' + id + '" data-control="checkbox-dropdown">' + 
    '<label class="dropdown-label">Select</label>'+ 
    '<div class="dropdown-list"> <a href="#" data-toggle="check-all" class="dropdown-option"> Check All </a>'

    for (i in options) {
        code = code + '<label class="dropdown-option">' +
        '<input type="checkbox" onclick="update_filter_code()" name="dropdown-group" value="' + options[i].name + '" id="' + id + "_" + options[i].id + '" checked/>' +
        options[i].name + '&nbsp| </label>'
    }

    code = code + "</div> </div>"
    parent.innerHTML += code
}
function convertBase(str, fromBase, toBase) {

    const DIGITS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/";

    const add = (x, y, base) => {
        let z = [];
        const n = Math.max(x.length, y.length);
        let carry = 0;
        let i = 0;
        while (i < n || carry) {
            const xi = i < x.length ? x[i] : 0;
            const yi = i < y.length ? y[i] : 0;
            const zi = carry + xi + yi;
            z.push(zi % base);
            carry = Math.floor(zi / base);
            i++;
        }
        return z;
    }

    const multiplyByNumber = (num, x, base) => {
        if (num < 0) return null;
        if (num == 0) return [];

        let result = [];
        let power = x;
        while (true) {
            num & 1 && (result = add(result, power, base));
            num = num >> 1;
            if (num === 0) break;
            power = add(power, power, base);
        }

        return result;
    }

    const parseToDigitsArray = (str, base) => {
        const digits = str.split('');
        let arr = [];
        for (let i = digits.length - 1; i >= 0; i--) {
            const n = DIGITS.indexOf(digits[i])
            if (n == -1) return null;
            arr.push(n);
        }
        return arr;
    }

    const digits = parseToDigitsArray(str, fromBase);
    if (digits === null) return null;

    let outArray = [];
    let power = [1];
    for (let i = 0; i < digits.length; i++) {
        digits[i] && (outArray = add(outArray, multiplyByNumber(digits[i], power, toBase), toBase));
        power = multiplyByNumber(fromBase, power, toBase);
    }

    let out = '';
    for (let i = outArray.length - 1; i >= 0; i--)
        out += DIGITS[outArray[i]];

    return out;
}
function update_filter_boxes(new_f_bin) {

}
function get_filter_string() {
	const cols = ["D", "R1", "R2", "R3"]
    data = []
    data.length = 4 * 9 * 33
    for (let z = 0; z <= 3; z++) {
        for (let y = 0; y <= 8; y++) {
            for (let x = 0; x <= 32; x++) {
                id = cols[z] + "_" + y.toString() + "_" + x.toString() 
                box_id = document.getElementById(id)
                if (box_id == null) {data[(z*9*33) +(y*33) + x] = "0"} 
                else {
                if (box_id.checked == true) {
                    data[(z*9*33) +(y*33) + x] = "1" } else {
                    data[(z*9*33) +(y*33) + x] = "0" }
            }
            } 
        }
    }
str =  BigInt('0b' + data.join("")).toString(36)
return [str ,convertBase(data.join(""), 2, 62)]
}

function update_filter_boxes(new_f_bin) {
    new_data = new_f_bin.split('')
    buff_len = 4 * 9 * 33 - new_data.length
    index = 0
    for (let z = 0; z <= 3; z++) {
        for (let y = 0; y <= 8; y++) {
            parent_id = cols[z] + "_" + y.toString()
            parent = document.getElementById(parent_id)
            for (let x = 0; x <= 32; x++) {
                id = cols[z] + "_" + y.toString() + "_" + x.toString() 
                box_id = document.getElementById(id)
                if (box_id != null)  {
                    if (buff_len <= index) {
                        if (new_data[index-buff_len] == '1'){
                            box_id.checked = true
                        } else{
                            box_id.checked = false
                        }
                    } else {
                        box_id.checked = false
                    }
                    box_id.dispatchEvent(new Event('change'))
                }
                index++
            }   
        }
    } 
    update_filter_code()

}
function update_filter_code(){
    new_f_codes = get_filter_string()
    document.getElementById("filter_code").value = new_f_codes[1]
}

function toggle_slider(slider_id){
    var x = document.getElementById(slider_id);
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }

}

function validate_filter_code(){
    new_f_code = document.getElementById("filter_code").value
    new_f_bin = convertBase(new_f_code, 62, 2)
    new_bin_code = BigInt('0b'+ new_f_bin)
    max_bin_code = BigInt('0b'+convertBase(max_f_codes[1], 62, 2))        
    if ((new_bin_code  & (~max_bin_code)) > 0n){
        alert("Invalide Filter code")
        update_filter_code()
    } else{
        update_filter_boxes(new_f_bin)
    }
}
var max_f_codes

(function($){
    
    
    cols = ["D", "R1", "R2", "R3"]
    for (j in cols) {
        create_drop_down("opt_"+cols[j], "Primary_Class", cols[j] +"_0", search_opt.Class)
        create_drop_down("opt_"+cols[j], "Sub_Class", cols[j] +"_1", search_opt.Class)
        create_drop_down("opt_"+cols[j], "Profession", cols[j] +"_2", search_opt.Profession)
        create_drop_down("opt_"+cols[j], "Passive_1", cols[j] +"_3", search_opt.Skills)
        create_drop_down("opt_"+cols[j], "Passive_2", cols[j] +"_4", search_opt.Skills)
        create_drop_down("opt_"+cols[j], "Active_1", cols[j] +"_5", search_opt.Skills)
        create_drop_down("opt_"+cols[j], "Active_2",cols[j] +"_6", search_opt.Skills)
        create_drop_down("opt_"+cols[j], "Stats 1",cols[j] +"_7", search_opt.Stats)
        create_drop_down("opt_"+cols[j], "Stats 2",cols[j] +"_8", search_opt.Stats)
    }
    max_f_codes = get_filter_string()
    document.getElementById("filter_code").value = max_f_codes[1]

})(jQuery);

$("#gen_slider").ionRangeSlider({
	type: "double",
	grid: false,
    skin : "square",
	min: 0,
	max: 11,
	from: 0,
	to: 11,
	step: 1,
	prefix: "Gen ",
});

$("#summon_slider").ionRangeSlider({
	type: "double",
	grid: false,
    skin : "square",
	min: 1,
	max: 10,
	from: 1,
	to: 10,
	prefix: "Summons left ",
});
