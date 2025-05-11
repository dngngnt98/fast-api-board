<script>
    import fastapi from "../lib/api";
    import Error from "../components/Error.svelte"
    export let params = {}
    let question_id = params.question_id
    let question = {answers:[]}
    let content = ""
    let error = {detail:[]}

    function get_question() {
        fastapi("GET", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()
        let url = "/api/answer/create/" + question_id
        let params = {
            content: content
        }
        fastapi("POST", url, params, (json) => {
            content = ''
            error = {detail:[]}
            get_question()
        },(err_json) => {
            error = err_json
        })
    }
</script>

<div class="container my-3">
    <!-- question -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line">
                {question.content}
            </div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {question.created_ad}
                </div>
            </div>
        </div>
    </div>
    <!--  answer list  -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}</h5>
    {#each question.answers as answer}
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">
                {answer.content}
            </div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {answer.created_at}
                </div>
            </div>
        </div>
    {/each}
    <!-- answer submit -->
    <Error error="{error}"/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} class="form-control"></textarea>
        </div>
        <input type="submit" value="등록" class="btn btn-primary" on:click="{post_answer}"/>
    </form>
</div>

<style>
    textarea {
        width: 100%;
    }
    form {
        text-align: right;
    }
    input[type=submit] {
        margin-top: 10px;
        font-size: 15px;
    }
</style>