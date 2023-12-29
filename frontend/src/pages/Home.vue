<script>
</script>

<template>
    <UnauthUser />
    <div class="welcome_wrapper">
        <h1 class="title">
            PNetwork
        </h1>
        <h2 class="under_title">
            create your own private social network
        </h2>
    </div>
</template>

<style scoped>
.welcome_wrapper {
    margin-top: 60px;

    font-family: Inter;
    color: #000;
    
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 10px;

}


.title {
    font-size: 90px;
    font-style: normal;
    font-weight: 100;
    line-height: normal;

    margin: 0px;
}

.under_title {
    font-size: 60px;
    font-style: normal;
    font-weight: 100;
    line-height: normal;

    text-align: center;
    margin: 0px;
    max-width: 600px;
}


</style>