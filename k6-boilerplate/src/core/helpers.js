function randomIntBetween(min, max) { // min and max included
  return Math.floor(Math.random() * (max - min + 1) + min);
}

function randomItem(arrayOfItems) {
  return arrayOfItems[Math.floor(Math.random() * arrayOfItems.length)];
}

function randomString(length) {
  const charset = 'abcdefghijklmnopqrstuvwxyz';
  let res = '';
  while (length--) res += charset[(Math.random() * charset.length) | 0];
  return res;
}

function findBetween(content, left, right) {
  let start = content.indexOf(left);
  if (start === -1) {
    return '';
  }
  start += left.length;
  const end = content.indexOf(right, start);
  if (end === -1) {
    return '';
  }
  return content.substring(start, end);
}

export { findBetween, randomIntBetween, randomItem, randomString,  };
