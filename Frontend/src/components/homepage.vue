<template>
    <div class="homepage">
        <h1>Welcome to CryptoDream</h1>
        <h2>Your Crypto Dashboard</h2>

        <div class="content">
            <div class="news-section">
                <h3>Latest Crypto News</h3>
                <ul>
                    <li v-for="news in newsList" :key="news.url">
                        <a :href="news.url" target="_blank">{{ news.title }}</a>
                    </li>
                </ul>
            </div>

            <div class="coin-list">
                <h3>Your Basket</h3>
                <div v-for="coin in basket" :key="coin.id" class="coin-card" @click="selectCoin(coin)">
                    <h3>{{ coin.name }}</h3>
                    <img :src="coin.image" :alt="coin.name" class="coin-image" />
                </div>
            </div>

            <div class="coin-details">
                <div v-if="selectedCoin">
                    <h3>{{ selectedCoin.name }} Details</h3>
                    <p><strong>Symbol:</strong> {{ selectedCoin.symbol.toUpperCase() }}</p>
                    <p><strong>Price:</strong> ${{ selectedCoin.current_price }}</p>
                    <p><strong>Market Cap:</strong> ${{ selectedCoin.market_cap }}</p>
                    <p><strong>24h Change:</strong> {{ selectedCoin.price_change_percentage_24h }}%</p>
                    <p><strong>High 24h:</strong> ${{ selectedCoin.high_24h }}</p>
                    <p><strong>Low 24h:</strong> ${{ selectedCoin.low_24h }}</p>
                    <img :src="selectedCoin.image" :alt="selectedCoin.name" class="coin-image" />
                    <GraphComponent :coinName="selectedCoin.name"/>
                    
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import GraphComponent from './GraphComponent.vue';

export default {
    name: 'Homepage',
    data() {
        return {
            basket: [],
            selectedCoin: null,
            newsList: []
        };
    },
    methods: {
        fetchCryptoData() {
            axios.get('https://api.coingecko.com/api/v3/coins/markets', {
                headers: {
                    'Access-Control-Allow-Origin': '*', // CORS header
                    'Access-Control-Allow-Methods': 'GET, OPTIONS', // Allow GET and OPTIONS methods
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization' // Allow specified headers
                },
                params: {
                    vs_currency: 'usd',
                    order: 'market_cap_desc',
                    per_page: 10,
                    page: 1,
                    sparkline: false
                }
            }).then(response => {
                console.log("API Response: ", response.data);
                this.basket = response.data;
            }).catch(error => {
                console.error("Error fetching crypto data:", error);
            });
        },

        fetchCryptoNews() {
            const apiKey = '78bdb3c0d9244bf8af87008703cde324';
            axios.get('https://newsapi.org/v2/everything', {
                params: {
                    q: 'cryptocurrency OR bitcoin OR ethereum OR tether OR bnb OR solana OR usdc OR cardano OR xrp OR polkadot OR litecoin OR chainlink',
                    language: 'en',
                    apiKey: apiKey
                }
            })
            .then(response => {
                this.newsList = response.data.articles.slice(0, 15); 
            })
            .catch(error => {
                console.error("Error fetching news:", error);
            });
        },

        selectCoin(coin) {
            this.selectedCoin = coin;
        }
    },
    components: {
        GraphComponent
    },
    mounted() {
        this.fetchCryptoData();
        this.fetchCryptoNews();
    }
};
</script>

<style scoped>
.homepage {
    text-align: center;
    background-color: #0a1829;
    color: white;
    padding: 20px;
}

.content {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}


.news-section {
    width: 30%;
    padding: 10px;
    border-right: 1px solid #ddd;
    background-color: #1a2534;
}

.news-section h3 {
    margin-bottom: 10px;
}

.news-section ul {
    list-style: none;
    padding: 0;
}

.news-section li {
    margin: 8px 0;
}

.news-section a {
    text-decoration: none;
    color: #00b8ff;
}

.news-section a:hover {
    text-decoration: underline;
}

.coin-list {
    width: 30%;
    text-align: center;
    background-color: #1a2534;
    padding: 20px;
    border-radius: 10px;
}

.coin-card {
    border: 1px solid #ddd;
    padding: 10px;
    margin: 10px;
    cursor: pointer;
    transition: background 0.3s;
}

.coin-card:hover {
    background: #8a8989;
}

.coin-image {
    width: 80px;
    display: block;
    margin: 5px auto;
}

.coin-details {
    width: 30%;
    padding: 20px;
    border-left: 1px solid #ddd;
    background-color: #1a2534;
    color: white;
    text-align: center;
    border-radius: 10px;
}

.coin-details img {
    width: 100px;
    margin-top: 10px;
}
</style>