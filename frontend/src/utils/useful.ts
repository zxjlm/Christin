export const waitTime = (time: number = 100) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true);
    }, time);
  });
};

export const hashCode = (s: string) =>
  s.split('').reduce((a, b) => {
    // eslint-disable-next-line no-param-reassign,no-bitwise
    a = (a << 5) - a + b.charCodeAt(0);
    // eslint-disable-next-line no-bitwise
    return a & a;
  }, 0);

/**
 * list-dict类型的去重
 * @param arr
 * @param key 去重的key
 */
export const dictUnique = (arr: any[], key: string): any[] => {
  const ret: any = {};
  const result = [];
  arr.forEach((elem) => {
    ret[elem[key]] = elem;
  });
  // eslint-disable-next-line no-restricted-syntax
  for (const retKey in ret) {
    if (ret.hasOwnProperty(retKey)) result.push(ret[retKey]);
  }
  return result;
};

/**
 * 边去重
 * @param arr
 */
export const edgesUnique = (arr: { source: string; target: string }[]) => {
  let tmp = arr.map((elem) => ({ ...elem, sum: elem.source + elem.target }));
  tmp = dictUnique(tmp, 'sum');
  return tmp.map((elem) => ({ source: elem.source, target: elem.target }));
};

/**
 * 一般性列表去重
 * @param arr
 */
export const normalUnique = (arr: any[]) => {
  return Array.from(new Set(arr));
};

/**
 * 数组相减的方法 - 使用es新特性
 * @param {Array} a
 * @param {Array} b
 */
export const arrSubtraction = (a: string[], b: string[]) => {
  if (Array.isArray(a) && Array.isArray(b)) {
    return a.filter((i) => !b.includes(i));
  }
  throw new Error('arrSubtraction(): Wrong Param Type');
};
