<template>
    <bk-navigation :default-open="false"
        navigation-type="top-bottom"
        :header-title="headerTitle"
        :side-title="title"
        :need-menu="true"
        @toggle="handleToggle"
        class="bk-wrapper">
        <!--      头部菜单      -->
        <template slot="header">
            <top-header></top-header>
        </template>
        <template slot="side-icon" class="monitor-logo">
            <img class="monitor-logo-icon" :src="imgPath">
            <div class="logo-title" @click="redirectHome">
                <span class="actual-text">&nbsp;任务调度平台&nbsp;</span>
                <span class="hover-text" aria-hidden="true">&nbsp;任务调度平台&nbsp;</span>
            </div>
        </template>
        <!--      左侧菜单      -->
        <template slot="menu">
            <leftMenu ref="leftMenu"></leftMenu>
        </template>
        <template slot="footer">
            <footer class="monitor-navigation-footer">
                <div>Copyright © 2022 Charles Xie. All Rights Reserved. V1.0.0</div>
            </footer>
        </template>
        <!--      内容区域      -->
        <container>
        </container>

    </bk-navigation>
</template>

<script>
    import topHeader from './header.vue'
    import leftMenu from './leftMenu.vue'
    import container from './container.vue'

    export default {
        components: {
            topHeader,
            leftMenu,
            container
        },
        data() {
            return {
                title: '',
                headerTitle: '',
                imgSrc: '',
            }
        },
        computed: {
            imgPath() {
                return require('@/assets/base/img/execute.png')
            }
        },
        created() {
            // this.initLogo()
        },
        mounted() {
            const defaultTableHeight = document.documentElement.clientHeight - 52 - 40
            this.$store.commit('setDefaultTableHeight', defaultTableHeight)
        },
        methods: {
            handleToggle(v) {
                this.$nextTick(() => {
                    this.$refs.leftMenu.nav.toggle = v
                })
            },
            redirectHome() {
                this.$router.push({name: 'home'})
            }
        }
    }
</script>

<style lang="scss" scoped>
.monitor-logo {
    width: 32px;
    height: 32px;
}

.monitor-logo-icon {
    width: 32px;
    height: 32px;
}
</style>
<style lang="scss">
.bk-wrapper {
    .bk-navigation-wrapper {
        .navigation-container {
            //max-width: calc(100% - 60px) !important;
            .container-content {
                padding: 0;
                display: flex;
                flex-direction: column;
            }
        }
    }

    .bk-navigation-header {
        background-color: #ffffff !important;
        border-bottom: 1px solid #dcdee4;
    }

    .monitor-navigation-footer {
        color: #979BA5;
        font-size: 12px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
}
.bk-navigation-title .title-icon {
    flex: 0 0 190px !important;
}

.logo-title {
    color: #313238;
    font-size: 20px;
    --border-right: 0;
    //--text-stroke-color: rgba(255, 255, 255, 0.6);
    --animation-color: #c33779;
    --fs-size: 2em;
    letter-spacing: 3px;
    text-decoration: none;
    position: relative;
    //color: transparent;
    //-webkit-text-stroke: 1px var(--text-stroke-color);
}

.hover-text {
    position: absolute;
    box-sizing: border-box;
    content: "";
    color: var(--animation-color);
    width: 0;
    inset: 0;
    border-right: var(--border-right) solid var(--animation-color);
    overflow: hidden;
    transition: 0.42s;
    -webkit-text-stroke: 1px var(--animation-color);
}
/* hover */
.logo-title:hover .hover-text {
    cursor: pointer;
    width: 100%;
    filter: drop-shadow(0 0 23px var(--animation-color));
}
</style>
