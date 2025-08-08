function convertToPersianDigits(input) {
    const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return input.toString().replace(/\d/g, (match) => persianDigits[match]);
}
let englishNumber = "12345";
let persianNumber = convertToPersianDigits(englishNumber);
console.log(persianNumber)
