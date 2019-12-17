const express = require('express')
const { WebhookClient } = require('dialogflow-fulfillment')
const app = express()
const fetch = require('node-fetch')
const base64 = require('base-64')

let username = "";
let password = "";
let token = "";
let categories = "";
let oneCate = "";
let products = [];
let totalPrice = 0;
let productMap = {}; // id : item
let productId = 0;
let productDescription = "";
let productReviews = "";
let productRatings = 0;
let productName = "";
let message = "";


//////////////////////////////////////////////////////////////////////////////////////////////////////
async function getToken () {
  let request = {
    method: 'GET',
    headers: {'Content-Type': 'application/json',
              'Authorization': 'Basic '+ base64.encode(username + ':' + password)},
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/login',request)
  const serverResponse = await serverReturn.json()
  token = serverResponse.token
  console.log("token is: "+token)
  return token;
}

async function redirectToHome () {
  let bd = {"page": "/" + username};
  let request = {
    method: 'PUT',
    headers: {'Content-Type': 'application/json',
              'x-access-token': token},
    body: JSON.stringify(bd),
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/application',request)
}

async function getAllCategories () {
  let request = {
    method: 'GET',
    headers: {'Content-Type': 'application/json', },
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/categories/',request)
  const serverResponse = await serverReturn.json()
  categories = serverResponse.categories
  console.log("categories are: ", categories)
  return categories;
}

async function getAllTags (oneCate) {
  let request = {
    method: 'GET',
    headers: {'Content-Type': 'application/json', },
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/categories/' + oneCate + '/tags', request)
  const serverResponse = await serverReturn.json()
  tags = serverResponse.tags
  console.log("tags are: ", tags)
  return tags;
}

async function getOneCategory (oneCate) {
  console.log("oneCate: ", oneCate)
  var bd = {};
  if (oneCate === "home") {
    bd = {"page": "/" + username};
  }
  else {
  bd = {"page": "/" + username + '/' + oneCate};
  }
  let request = {
    method: 'PUT',
    headers: {'Content-Type': 'application/json',
              'x-access-token': token},
    body: JSON.stringify(bd),
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/application', request)
}

async function getCartDetails () {
    let request = {
    method: 'GET',
    headers: {'Content-Type': 'application/json',
              'x-access-token': token},
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/application/products', request)
  const serverResponse = await serverReturn.json()
  products = serverResponse.products
  // console.log("products are: ", products)
  return products;
}


async function getProductMap () {
  let request = {
    method: 'GET',
    headers: {'Content-Type': 'application/json',},
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/products', request)
  const serverResponse = await serverReturn.json()
  let tempProducts = serverResponse.products
  tempProducts.forEach(prod => productMap[prod.name] = prod);
  console.log("productMap generated")
}

async function goToProductDetail (productName) {
  productId = productMap[productName]["id"]
  productDescription = productMap[productName]["description"];
  console.log('productName:', productName)
  console.log('productId:', productId)
  console.log("productDescription is: ", productDescription)
  return productDescription;
}

async function goToProductReviewsAndRatings (productName) {
  productId = productMap[productName]["id"]
  console.log("productId:", productId)
  let request = {
    method: 'GET',
    headers: {'Content-Type': 'application/json',},
    redirect: 'follow'
  }
  const serverReturn = await fetch('https://mysqlcs639.cs.wisc.edu/products/' + productId + '/reviews/', request)
  const serverResponse = await serverReturn.json()
  let reviews = serverResponse.reviews;
  console.log("reviews:", reviews)
  productReviews = "";
  reviews.forEach(rev => {
    productReviews = productReviews.concat(rev.text);
    productRatings += rev.stars;
  });
  productRatings = productRatings / reviews.length;

  let productReviewsAndRatings = "Reviews: " + productReviews + " / Average Rating:" + productRatings;
  console.log("productReviewsAndRatings: ", productReviewsAndRatings)
  return productReviewsAndRatings;
}

async function doAction (action, tagOrProduct, mode) {
  // mode: tag/cart
  let url = '';
  if (mode === "tag") {
    url = 'https://mysqlcs639.cs.wisc.edu/application/tags/' + tagOrProduct;
  }
  else if (mode === "cart" && tagOrProduct === -1) {
    url = 'https://mysqlcs639.cs.wisc.edu/application/products/';
  }
  else {
    url = 'https://mysqlcs639.cs.wisc.edu/application/products/' + tagOrProduct;
  }
  console.log("action:", action)
  console.log("tagOrProduct:", tagOrProduct)
  console.log("mode:", mode)

  let request = {
    method: action === "add" ? 'POST' : 'DELETE',
    headers: {'Content-Type': 'application/json',
      'x-access-token': token},
    redirect: 'follow'
  };
  const serverReturn = await fetch(url, request)
  const serverResponse = await serverReturn.json()
  message = serverResponse.message;
  console.log("message:", message)
  return message;
}

async function clearMsg () {
  url = 'https://mysqlcs639.cs.wisc.edu//application/messages';
  let request = {
    method: 'DELETE',
    headers: {'Content-Type': 'application/json',
      'x-access-token': token},
    redirect: 'follow'
  };
  const serverReturn = await fetch(url, request)
  const serverResponse = await serverReturn.json()
  message = serverResponse.message;
  console.log("message:", message)
}

async function addMsg (person, msg) {
  // person: agent/human
  let bd = {
    "date": new Date('October 15, 1996 05:35:32').toISOString(),
    "isUser": person === "agent" ? false : true,
    "text": msg,
    "id": 0,
  };

  url = 'https://mysqlcs639.cs.wisc.edu//application/messages';
  let request = {
    method: 'POST',
    headers: {'Content-Type': 'application/json',
      'x-access-token': token},
    body: JSON.stringify(bd),
    redirect: 'follow'
  };
  const serverReturn = await fetch(url, request)
  const serverResponse = await serverReturn.json()
  message = serverResponse.message;
  console.log("message:", message)
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
app.get('/', (req, res) => res.send('online'))
app.post('/', express.json(), (req, res) => {
  const agent = new WebhookClient({ request: req, response: res })
  async function welcome () {
    let output = 'Webhook works!';
    agent.add(output)
    await addMsg("agent", output);
  }

  
  async function login () {
    // You need to set this from `username` entity that you declare in DialogFlow
    username = agent.parameters.username;
    // You need to set this from password entity that you declare in DialogFlow
    password = agent.parameters.password;
    await addMsg("human", agent.query);
    console.log('username:', username);
    console.log('password:', password);
    token = await getToken();
    await clearMsg();  // Note this line has to be after getting a token
    await redirectToHome();
    let output = 'token:' + token;
    agent.add(token)
    await addMsg("agent", output);
  }

  async function category () {
    categories = await getAllCategories();
    let output = categories.join(', ') + " / Type 'go to [category]' to see more";
    agent.add(output);
    await addMsg("agent", output);
  }

  async function oneCategory () {
    oneCate = agent.parameters.category;
    await addMsg("human", agent.query);
    console.log('oneCate:', oneCate);
    await getOneCategory(oneCate);
  }

  async function tag () {
    tags = await getAllTags(oneCate);
    let output = tags.join(', ');
    agent.add(output)
    await addMsg("agent", output);
  }

  async function cart () {
    products = await getCartDetails();
    totalPriceFunc = obj => Object.values(products).reduce((a, b) => a.price + b.price);
    // Use reducer function when more than 1 products
    if (products.length > 1) {
      totalPrice = products.reduce(totalPriceFunc);
    }
    else {
      totalPrice = products[0]["price"];
    }
    let productDetail = "";
    Object.values(products).forEach(prod => 
      productDetail = productDetail.concat(prod["name"] + " " + prod["count"] + "; "
    ));
    console.log('Total price in cart is: ', totalPrice);
    let output = 'Total price in cart is: ' + totalPrice + ' / ' + productDetail + ' / To confirm, enter "confirm"';
    agent.add(output)
    await addMsg("agent", output);
  }

  async function productDetail () {
    // getProductMap first
    await getProductMap();

    productName = agent.parameters.product;
    await addMsg("human", agent.query);
    productDescription = await goToProductDetail(productName);
    let output = 'Description: ' + productDescription;
    agent.add(output)
    await addMsg("agent", output);
  }

  async function reviewsAndRatings () {
    productReviewsAndRatings = await goToProductReviewsAndRatings(productName);
    let output = productReviewsAndRatings;
    agent.add(output)
    await addMsg("agent", output);
  }

  async function actionTag () {
    let action = agent.parameters.action;
    let tag = agent.parameters.tag;
    await addMsg("human", agent.query);
    message = await doAction(action, tag, "tag");
    let output = message;
    agent.add(output)
    await addMsg("agent", output);
  }

  async function actionCart () {
    // getProductMap first, just in case
    await getProductMap();

    let action = agent.parameters.action;
    let productName = agent.parameters.product;
    await addMsg("human", agent.query);
    let productId = productMap[productName]["id"];
    message = await doAction(action, productId, "cart");
    let output = message;
    agent.add(output)
    await addMsg("agent", output);
  }

  async function actionCartClear () {
    message = await doAction("clear", -1, "cart");
    let output = message;
    agent.add(output)
    await addMsg("agent", output);
  }

  async function actionCartConfirm () {
    await getCart();
    let confirm = agent.parameters.confirm;
    await addMsg("human", agent.query);
    let output = 'confimation status:' + confirm;
    agent.add(output)
    await addMsg("agent", output);
  }

  let intentMap = new Map()
  intentMap.set('Default Welcome Intent', welcome)
  // You will need to declare this `Login` content in DialogFlow to make this work
  intentMap.set('login', login) 
  intentMap.set('category', category) 
  intentMap.set('category - oneCate', oneCategory) 
  intentMap.set('tag', tag) 
  intentMap.set('cart', cart) 
  intentMap.set('productDetail', productDetail) 
  intentMap.set('productDetail - reviewsAndRatings', reviewsAndRatings) 
  intentMap.set('actionTag', actionTag) 
  intentMap.set('actionCart', actionCart) 
  intentMap.set('actionCartClear', actionCartClear) 
  intentMap.set('cart - confirm', actionCartConfirm) 
  
  agent.handleRequest(intentMap)
})

app.listen(process.env.PORT || 8080)
