<script>
    import {push} from 'svelte-spa-router'
    import fastapi from '../lib/api'
    import Error from '../components/Error.svelte'

    export let params = {}
    const question_id = params.question_id

    let error = {detail:[]}
    let subject = ''
    let content = ''

    fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
        subject = json.subject
        content = json.content
    })

    function update_question(event) {
        event.preventDefault()

        let url = "/api/question/update/"
        let params = {
            question_id: question_id,
            subject: subject,
            content: content
        }

        fastapi("put", url, params, (json) => {
            push('/detail/' + question_id)
        }, (json_error) => {
            error = json_error
        })
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pd-2">수정</h5>
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input bind:value="{subject}" class="form-control" id="subject">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea bind:value="{content}" class="form-control" id="content" rows="10"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_question}">수정</button>
    </form>
</div>