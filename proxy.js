function proxyAll(target, name = "") {
    // 创建一个递归代理函数
    function recursiveProxy(prefix, obj) {
        return new Proxy(obj, {
            get(target, prop, receiver) {
                console.log(`GET ${prefix}.${prop}`);
                const value = Reflect.get(target, prop, receiver);
                return typeof value === 'object' && value !== null ? recursiveProxy(`${prefix}.${prop}`, value) : value;
            }, set(target, prop, value, receiver) {
                console.log(`SET ${prefix}.${prop} = ${value}`);
                return Reflect.set(target, prop, value, receiver);
            }, has(target, prop) {
                console.log(`HAS ${prefix}.${prop}`);
                return Reflect.has(target, prop);
            }, deleteProperty(target, prop) {
                console.log(`DELETE ${prefix}.${prop}`);
                return Reflect.deleteProperty(target, prop);
            }, defineProperty(target, prop, descriptor) {
                console.log(`DEFINE PROPERTY ${prefix}.${prop}`);
                return Reflect.defineProperty(target, prop, descriptor);
            }, ownKeys(target) {
                console.log(`OWN KEYS`);
                return Reflect.ownKeys(target);
            }, preventExtensions(target) {
                console.log(`PREVENT EXTENSIONS`);
                return Reflect.preventExtensions(target);
            }, isExtensible(target) {
                console.log(`IS EXTENSIBLE`);
                return Reflect.isExtensible(target);
            }, getPrototypeOf(target) {
                console.log(`GET PROTOTYPE OF`);
                return Reflect.getPrototypeOf(target);
            }, setPrototypeOf(target, prototype) {
                console.log(`SET PROTOTYPE OF`);
                return Reflect.setPrototypeOf(target, prototype);
            }, construct(target, argumentsList, newTarget) {
                console.log(`CONSTRUCT`);
                return Reflect.construct(target, argumentsList, newTarget);
            }, apply(target, thisArg, argumentsList) {
                console.log(`APPLY`);
                return Reflect.apply(target, thisArg, argumentsList);
            }
        });
    }

    // 对初始目标对象进行递归代理
    return recursiveProxy(name, target);
}