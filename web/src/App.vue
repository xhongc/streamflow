<template>
    <div id="app">
        <magic-menu></magic-menu>
    </div>
</template>

<script>
    import magicMenu from '@/components/base/magicMenu'

    export default {
        name: 'app',
        components: {
            magicMenu
        },
        data() {
            return {
                menuList: []
            }
        },
        created() {
            this.getHeight()
        },
        methods: {
            getHeight() {
                const headerHeight = 60
                if (window.innerHeight) {
                    this.winHeight = window.screen.availHeight - (window.outerHeight - window.innerHeight)
                }
                // if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
                //     this.winHeight = document.documentElement.clientHeight;
                // }
                this.winHeight = this.winHeight - headerHeight + 'px'
            }
        }
    }
</script>
<style lang="scss">
html,
body {
    height: 100%;
    min-width: 1280px;
}

::-webkit-scrollbar-thumb:window-inactive {
    background: rgba(255, 0, 0, .4)
}

::-webkit-scrollbar {
    width: 6px;
    height: 8px;
    background-color: rgba(255, 255, 255, .07)
}

::-webkit-scrollbar-thumb {
    -webkit-border-radius: 10px;
    border-radius: 10px;
    background: rgba(17, 64, 108, 0.5);
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .5)
}

::-webkit-scrollbar-thumb:window-inactive {
    background-color: rgba(255, 255, 255, .07)
}

.pm-title {
    margin-left: 10px;

    .pm-title-block {
        width: 20px;
        height: 22px;
        margin-top: 2px;
        float: left;
    }

    .ivu-icon-md-settings {
        font-size: 22px;
        color: #1facdd;
    }
}

.pm-top {
    border: 1px solid rgb(227, 227, 227);
    background-color: white;
    height: 80px;

    > div {

        > div,
        > span,
        > button {
            vertical-align: middle;
        }
    }
}

.base {
    position: absolute;
    width: 98%;
    left: 1%;
    top: 42px;
    padding: 10px;
    z-index: 9;
    border: 1px solid #e3e3e3;
    font-size: 0;
    text-align: center;

    .base_box {
        display: inline-block;
        padding-right: 30px;
        vertical-align: top;

        > span {
            display: inline-block;
            font-size: 12px;
            float: left;
            line-height: 32px;
            height: 64px;
            overflow: auto;
        }
    }
}

button.bk-primary {
    background-color: rgb(17, 64, 108) !important;
    border-color: rgb(17, 64, 108) !important;
}

button.bk-button-text {
    background-color: transparent !important;
}

.bk-form-checkbox.is-checked .bk-checkbox {
    border-color: rgb(17, 64, 108) !important;
    background-color: rgb(17, 64, 108) !important;
    background-clip: border-box !important;
}

.bk-button-group .bk-button.is-selected {
    border-color: rgb(17, 64, 108) !important;
    color: rgb(17, 64, 108) !important;
}

.bk-button.bk-default:hover {
    border-color: rgb(17, 64, 108) !important;
    color: rgb(17, 64, 108) !important;
}

.bk-form-radio input[type=radio].is-checked {
    color: rgb(17, 64, 108) !important;
}

.bk-steps .bk-step.current .bk-step-icon, .bk-steps .bk-step.current .bk-step-number, .bk-steps .bk-step.current .bk-step-text {
    border-color: rgb(17, 64, 108) !important;
    background-color: rgb(17, 64, 108) !important;
}

.bk-steps .bk-step.done .bk-step-icon, .bk-steps .bk-step.done .bk-step-number, .bk-steps .bk-step.done .bk-step-text {
    border-color: rgb(17, 64, 108) !important;
    color: rgb(17, 64, 108) !important;
}
</style>
