<script>
    import {link} from 'svelte-spa-router'
    import {page, access_token, email, is_login} from '../lib/store'
</script>

<!-- Navigation Bar -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/" on:click="{() => {$page = 0}}">게시판</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                {#if $is_login}
                    <li class="nav-item">
                        <a use:link href="/user-login" on:click={() => {
                            $access_token = ''
                            $email = ''
                            $is_login = false
                        }}>Log-out ({$email})</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-create">Sign Up</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login">Sign In</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>