<template>
    <div class="mx-auto w80">
        <NCard>
            <h3>Token Cost Calculator - Token耗费计算器</h3>
            <ul>
                <li>Token Cost Caclulator is a tool to help you how many tokens you need to pay for a LLM prompt. </li>
                <li class="text-grey">Token耗费计算器是一个帮助你计算大语言模型耗费多少Token的工具。</li>
                <li>We offer multiple models for you to choose, including GPT-3.5-turbo/GPT-4/HuggingFace and so on.</li>
                <li class="text-grey">我们提供了多个模型供你选择，包括GPT-3.5-turbo/GPT-4/HuggingFace等。</li>
                <li>You may use a thirdparty proxy to access final model, therefor we offer a ratio option for you to calculate the final cost.</li>
                <li class="text-grey">你可能会使用第三方API来访问最终接口，因此我们提供了一个倍率选项来计算最终的耗费。</li>
            </ul>
            <NDivider></NDivider>
            <div>
                <NGrid x-gap="12" :cols="2">
                    <NGi>
                        <NSelect
                            size="small"
                            placeholder="Select Copyright（选择厂商）"
                            clearable
                            bordered
                            v-model:value="copyright"
                            :options="copyrights"
                        />
                    </NGi>
                    <NGi>
                        <NSelect
                            size="small"
                            placeholder="Select Model（选择模型）"
                            clearable
                            bordered
                            v-model:value="model"
                            :options="get_copyright_models(copyright as keyof Copyright).map(
                                (item: any) => ({
                                    label: item,
                                    value: item
                                })
                            )"
                        />
                    </NGi>
                </NGrid>
                <NGrid x-gap="12" cols="3" class="mt5">
                    <NGi>
                        <NInputNumber
                            size="small"
                            placeholder="Input Ratio（输入比例）"
                            clearable
                            bordered
                            v-model:value="ratio"
                            :max="999"
                            :step="0.01"
                        >
                            <template #prefix>
                                <span>Ratio（倍率）</span>
                            </template>
                        </NInputNumber>
                    </NGi>
                    <NGi>
                        <NSwitch
                            size="small"
                            v-model:value="enableFunctions"
                        >
                            <template #checked>
                                <span>Enable Functions（启用函数）</span>
                            </template>
                            <template #unchecked>
                                <span>Disable Functions（禁用函数）</span>
                            </template>
                        </NSwitch>
                    </NGi>
                </NGrid>
                <NGrid x-gap="12" cols="5" class="mt5">
                    <NGi>
                        <NStatistic>
                            <template #label>
                                <span>Tokens</span>
                            </template>
                            <NNumberAnimation :precision="4" ref="numberAnimationInstRef" :from="0" :to="cost.token" :duration="1000" />
                        </NStatistic>
                    </NGi>
                    <NGi>
                        <NStatistic>
                            <template #label>
                                <span>耗费人民币</span>
                            </template>
                            <NNumberAnimation :precision="4" ref="numberAnimationInstRef1" :from="0" :to="cost.CNY * ratio" :duration="1000" />
                        </NStatistic>
                    </NGi>
                    <NGi>
                        <NStatistic>
                            <template #label>
                                <span>Cost USD</span>
                            </template>
                            <NNumberAnimation :precision="4" ref="numberAnimationInstRef2" :from="0" :to="cost.USD * ratio" :duration="1000"  />
                        </NStatistic>
                    </NGi>
                    <NGi>
                        <NStatistic>
                            <template #label>
                                <span>Cost EUR</span>
                            </template>
                            <NNumberAnimation :precision="4" ref="numberAnimationInstRef3" :from="0" :to="cost.EUR * ratio" :duration="1000"  />
                        </NStatistic>
                    </NGi>
                    <NGi>

                        <NStatistic>
                            <template #label>
                                <span>日本円を消費する</span>
                            </template>
                            <NNumberAnimation :precision="4" ref="numberAnimationInstRef4" :from="0" :to="cost.JPY * ratio" :duration="1000"  />
                        </NStatistic>
                    </NGi>
                </NGrid>
                <NGrid x-gap="12" cols="1" class="mt5">
                    <NGi>
                        <NText>Input Prompt（输入Prompt），Messgaes：</NText>
                        <NInput
                            class="mt5"
                            size="small"
                            placeholder="Input Prompt（输入Prompt），You can input all JSON format prompts here.（你可以在这里输入所有的JSON格式的Prompt）"
                            clearable
                            bordered
                            v-model:value="prompts"
                            type="textarea"
                            rows="8"
                        />
                    </NGi>
                </NGrid>
                <NGrid x-gap="12" cols="1" class="mt5" v-if="enableFunctions">
                    <NGi>
                        <NText>Input Prompt（输入Prompt），Functions：</NText>
                        <NInput
                            class="mt5"
                            size="small"
                            placeholder="Input Prompt（输入Prompt），You can input all JSON format prompts here.（你可以在这里输入所有的JSON格式的Prompt）"
                            clearable
                            bordered
                            v-model:value="functions"
                            type="textarea"
                            rows="8"
                        />
                    </NGi>
                </NGrid>
                <NGrid cols="1">
                    <NGi>
                        <NButton type="primary" class="mt5" @click="updateCost">Calculate（计算）</NButton>
                    </NGi>
                </NGrid>
            </div>
        </NCard>
    </div>
</template>

<script setup lang="ts">
import {
    NCard,
    NGrid, NGi,
    NDivider,
    NSelect, NSwitch,
    NInput, NInputNumber,
    NNumberAnimation,
    NStatistic,
    NButton,
    NText,
} from 'naive-ui'
import { ref } from 'vue'
import { api_token_cost } from '../interface/tokenizer'

const model = ref('GPT-3.5-turbo')
const copyright = ref('OpenAI')
const models = ref({
    'OpenAI' : [
        "GPT-3.5-turbo-0613",
        "GPT-3.5-turbo-16k-0613",
        "GPT-4-0314",
        "GPT-4-32k-0314",
        "GPT-4-0613",
        "GPT-4-32k-0613",
    ],
    'HuggingFace' : []
})
interface Copyright {
    OpenAI: string[],
    HuggingFace: string[],
}
const get_copyright_models = (copyright: keyof Copyright)=> {
    return models.value[copyright]
}

const copyrights = ref([{
    'label': 'OpenAI',
    'value': 'OpenAI'
},{
    'label': 'HuggingFace',
    'value': 'HuggingFace'
}])
const prompts = ref(`[{
    "role": "system",
    "text": "You are a well performing token cost calculator. you should tell how much token I need to pay for a LLM prompt."
},{
    "role": "user",
    "text": "prompt: jvav is the best programming language in the world."
}]`)
const enableFunctions = ref(false)
const functions = ref(`[{
    "name": "php",
    "description": "php is the best programming language in the world.",
    "parameters":{
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the person to greet."
            }
        },
        "required": ["name"]
    }
}]`)
const ratio = ref(1)

const cost = ref({
    'token': 0.0,
    'CNY': 114.0,
    'USD': 514.0,
    'EUR': 1919.0,
    'JPY': 810.0,
})

const updateCost = async () => {
    const result = await api_token_cost(prompts.value, enableFunctions.value ? functions.value : '', copyright.value, model.value) as any
    const converted = result.result as any
    cost.value.token = converted.token
    cost.value.CNY = parseFloat(converted.CNY)
    cost.value.USD = converted.USD
    cost.value.EUR = converted.EUR
    cost.value.JPY = converted.JPY
}

</script>