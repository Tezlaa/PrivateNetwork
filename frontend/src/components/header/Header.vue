<script>
import UnauthUser from './unauth/UnauthUser.vue';
import AuthUser from './auth/AuthUser.vue';

export default {
  components: {
    UnauthUser,
    AuthUser,
  },
};
</script>

<template>
    <header class="header">
        <div class="wrapper_header">
            <div class="left">
                <img src="/logo.png" alt="" style="width: 50px;">
                <h3>PNetwork</h3>
            </div>
            <div class="right">
                <UnauthUser />
                <button type="button" class="button-source">
                    <a href="https://github.com/Tezlaa/djangoChat_withSockets" target="_blank">
                        <img src="/github.png" alt="" srcset="">
                    </a>
                </button>
            </div>
        </div>
    </header>
    <hr>
</template>


<style>
.header {
    padding-left: 22px;
    padding-right: 22px;
    padding-top: 22px;
    padding-bottom: 11px;
    color: #595959;

    font-family: Inter;
    font-size: 20px;
    font-style: normal;
    font-weight: 300;
    line-height: normal;
}

.header h3 {
    font-size: 20px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
}

.header hr {
    background: #ABABAB;
    height: 1px;
    border: 0px;
}

.header .wrapper_header {
    display: flex;
    justify-content: space-between;
}

.header .left {
    display: flex;
    align-items: center;
    gap: 10px;
}
.header .button-source img {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
    opacity: 0.34;
}

.header .right {
    display: flex;
}

.header .right button {
    background-color: transparent;
    border: solid 0px;
    margin-left: 104px;
}

.header .right ul {
    display: flex;
    gap: 49px;
    list-style: none;
    justify-content: center;
}

.header .right ul a li {
    margin: auto;
    width: 70;
}

.header .right a {
    text-decoration: none;
    color: #595959;
}

</style>