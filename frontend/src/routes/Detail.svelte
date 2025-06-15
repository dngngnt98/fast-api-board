<script>
    import fastapi from "../lib/api";
    import Error from "../components/Error.svelte"
    import {link, push} from "svelte-spa-router"
    import {is_login, email} from "../lib/store"
    import moment from "moment/min/moment-with-locales"
    moment.locale('ko')

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

    function delete_question(_question_id) {
        if (window.confirm("정말로 삭제하시겠습니까?")) {
            let url = "/api/question/delete/"
            let params = {
                question_id: _question_id
            }

            fastapi("delete", url, params, (json) => {
                push('/')
            }, (err_json) => {
                error = err_json
            })
        }
    }

    function delete_answer(answer_id) {
        if(window.confirm("정말 해당 댓글을 삭제하시겠습니까?")) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: answer_id
            }

            fastapi("delete", url, params, (json) => {
                get_question()
            }, (err_json) => {
                error = err_json
            })
        }
    }
</script>

<div class="container my-3">
    <button class="btn btn-secondary mb-2" on:click="{() => {push('/')}}">
        목록
    </button>
    <!-- question -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line">
                {question.content}
            </div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {question.user ? question.user.username : ''}
                </div>
                {#if question.modified_at}
                <div class="badge bg-light text-dark p-2">
                    {moment(question.modified_at).format('YYYY-MM-DD HH:mm:ss')}
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2">
                    {moment(question.created_ad).format('YYYY-MM-DD HH:mm:ss')}
                </div>
            </div>
            <div class="my-3 text-end">
                {#if question.user && question.user.email === $email}
                    <a use:link href="/question-modify/{question.id}" class="btn btn-sm btn-outline-info">수정</a>
                    <button class="btn btn-sm btn-outline-danger" on:click={() => delete_question(question_id)}>
                        삭제
                    </button>
                {/if}
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
                    {answer.user ? answer.user.username : ''}
                </div>
                {#if answer.modified_at}
                <div class="badge bg-light text-dark p-2">
                    {moment(answer.modified_at).format('YYYY-MM-DD HH:mm:ss')}
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2">
                    {moment(answer.created_at).format('YYYY-MM-DD HH:mm:ss')}
                </div>
            </div>
            <div class="my-3">
                {#if answer.user && answer.user.email === $email}
                    <a use:link href="/answer-modify/{answer.id}"
                        class="btn btn-sm btn-outline-secondary">수정</a>
                    <button class="btn btn-sm btn-outline-danger" on:click={() => delete_answer(answer.id)}>삭제</button>
                {/if}
            </div>
        </div>
    {/each}
    <!-- answer submit -->
    <Error error="{error}"/>
    {#if $is_login}
        <form method="post" class="my-3">
            <div class="mb-3">
                <textarea rows="10" bind:value={content} class="form-control"></textarea>
            </div>
            <input type="submit" value="등록" class="btn btn-primary" on:click="{post_answer}"/>
        </form>
    {/if}
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