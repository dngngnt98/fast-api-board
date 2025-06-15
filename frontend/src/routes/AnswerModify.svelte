<script>
    import {push} from 'svelte-spa-router'
    import fastapi from '../lib/api';
    import Error from '../components/Error.svelte'

    export let params = {}
    const answer_id = params.answer_id

    let error = {detail:[]}
    let question_id = 0
    let content = ''

    fastapi("get", "/api/answer/detail/" + answer_id, {}, (json) => {
        question_id = json.question_id
        content = json.content
    })

    function update_answer(event) {
        event.preventDefault()
        let url = "/api/answer/update/"
        let params = {
            answer_id: answer_id,
            content: content
        }

        fastapi("put", url, params, (json) => {
            push("/detail/" + question_id)
        }, (err_json) => {
            error = err_json
        })
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pd-2">답변 수정</h5>
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea id="content" class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button on:click="{update_answer}" class="btn btn-primary">수정</button>
    </form>
</div>