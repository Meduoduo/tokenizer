import {
    createRouter,
    createWebHistory,
    RouteRecordRaw
} from 'vue-router'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/cost',
        component: () => import('../views/TokenizerCost.vue')
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router