import { api_base } from './base'
import { stringify } from 'querystring'

export const api_token_cost = (token: string, functions: string, copyright: string, model: string) =>
    api_base('/v1/token/cost', 'post', stringify({ token, functions, model, copyright }))