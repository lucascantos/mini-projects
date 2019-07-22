// const sayHello = (function (){
//     var message = 'Hello!'
//     function sayHello(){
//         console.log(message)

//     }
//     return sayHello
// })()

// const counter = (function(){
//     let count = 0

//     return{
//         inc: function() { count = count + 1},
//         get: function() { console.log(count)}
//     }
// })()

// counter.get()
// counter.inc()
// counter.get()

// const name = 'lucas'
// const last = 'cantos'


// const val = 42
// const arr = [
//     'sting',
//     42,
//     function(){
//         console.log('hi')
//     }
// ]

// arr[2]()
// console. log(typeof(val))


// const o = new Object()
// o.firstname = 'lucas'
// o.lastname = 'cantos'
// o.student = true
// o.greet = function(){
//     console.log('howdy!')
// }

// const o2 = {}

// console.log(o['firstname'])


// function makeFunctionArray(){
//     const arr = []

//     const message = 'Hello!'
//     for (let i = 0; i <5; i++){
//         arr.push( 
//             (function(x){
//                 return function (){
//                     console.log(x)
//                 }
//             })(i))
//     return arr
//     }
// }

// const functionArr = makeFunctionArray()
// functionArr[0]()