<template>
    <body class="body">
        <div class="container text-center">
            <homepage />
        </div>
    </body>
</template>

<script>
import homepage from '@/components/homepage.vue';

export default {
    name: 'HomepageView',
    components: {
        homepage,
    },
};
</script>

<style>
body {
    background: black;
    color: black;
}
</style>