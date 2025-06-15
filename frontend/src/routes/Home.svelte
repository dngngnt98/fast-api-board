<script>
    import fastapi from "../lib/api";
    import {link} from 'svelte-spa-router'
    import {page, keyword, is_login} from '../lib/store'
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    let question_list = []
    let size = 10
    let total = 0
    let key = ''
    $: total_page = Math.ceil(total / size)

    function get_question_list() {
        let params = {
            page: $page,
            size: size,
            keyword: $keyword,
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            total = json.total
            key = $keyword
        })
    }

    $:$page, $keyword, get_question_list()
</script>

<div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            {#if $is_login}
            <a use:link href="/question-create" class="btn btn-primary">질문 등록</a>
            {/if}
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{key}">
                <button class="btn btn-outline-secondary" on:click={() => {$keyword = key, $page = 0}}>
                    찾기
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="table-dark text-center">
            <th>번호</th>
            <th style="width: 50%">제목</th>
            <th>작성자</th>
            <th>등록일</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, index}
            <tr class="text-center">
                <td class="text-secondary">{total - ($page * size) - index}</td>
                <td class="text-start">
                    <a class="text-decoration-none text-secondary" use:link href="/detail/{question.id}">{question.subject}</a>
                    {#if question.answers.length > 0}

                        <span class="text-secondary small mx-2">
                            [{question.answers.length}]
                        </span>
                    {/if}
                </td>
                <td>
                    {question.user ? question.user.username : ''}
                </td>
                <td class="text-secondary">
                    {moment(question.created_at).format('YYYY-MM-DD HH:mm:ss')}
                </td>
            </tr>
        {/each}
        </tbody>
    </table>
    <!--  Paging  -->
    <ul class="pagination justify-content-center">
        <!-- first page -->
<!--        <li class="page-item {$page === 0 && 'disabled'}">-->
<!--            <button class="page-link" on:click="{() => get_question_list(0)}">-->
<!--                <span>&lt;&lt;</span>-->
<!--            </button>-->
<!--        </li>-->
        <!-- prev page -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">&lt;</button>
        </li>
        <!-- page number list -->
        {#each Array(total_page) as _, loop_page}
            {#if loop_page >= $page - 5 && loop_page <= $page + 5}
            <li class="page-item {loop_page === $page && 'active'}">
                <button class="page-link" on:click="{() => $page = loop_page}">{loop_page + 1}</button>
            </li>
            {/if}
        {/each}
        <!-- next page -->
        <li class="page-item {$page >= total_page - 1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">&gt;</button>
        </li>
        <!-- last page -->
<!--        <li class="page-item {$page === total_page - 1 && 'disabled'}">-->
<!--            <button class="page-link" on:click="{() => get_question_list(total_page - 1)}">&gt;&gt;</button>-->
<!--        </li>-->
    </ul>
</div>