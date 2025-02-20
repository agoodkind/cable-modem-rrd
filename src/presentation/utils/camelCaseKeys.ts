type Primitive = string | number | boolean | null | undefined;

type CamelCase<S extends string> =
  S extends `${infer P1}_${infer P2}${infer P3}`
    ? `${Lowercase<P1>}${Uppercase<P2>}${CamelCase<P3>}`
    : Lowercase<S>;

type KeysToCamelCase<T> = T extends Primitive
  ? T
  : T extends Array<infer U>
    ? Array<KeysToCamelCase<U>>
    : T extends object
      ? {
          [K in keyof T as CamelCase<string & K>]: KeysToCamelCase<T[K]>;
        }
      : never;

function toCamelCase(str: string): string {
  return str.replace(/([-_][a-z])/g, (group) =>
    group.toUpperCase().replace("-", "").replace("_", ""),
  );
}

export function deepCamelCaseKeys<T>(obj: T): KeysToCamelCase<T> {
  if (Array.isArray(obj)) {
    return obj.map((item) => deepCamelCaseKeys(item)) as KeysToCamelCase<T>;
  } else if (obj !== null && typeof obj === "object") {
    return Object.keys(obj).reduce((result, key) => {
      const value = obj[key as keyof typeof obj];
      const camelKey = toCamelCase(key) as keyof KeysToCamelCase<T>;
      (result as any)[camelKey] = deepCamelCaseKeys(value);
      return result;
    }, {} as KeysToCamelCase<T>);
  }
  return obj as KeysToCamelCase<T>;
}
