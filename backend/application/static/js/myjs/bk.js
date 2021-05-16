function update_progress(progress_msg_div, now_state = '') {
    let spinner = '<div class="spinner-grow spinner-grow-sm" role="status" id="neo-spinner">' +
        '  <span class="sr-only">Loading...</span>' +
        '</div>'
    let success = '<em class="icon ni ni-list-check"></em>'
    let url = api_for_sandbox_progress.replace('none', task_id)

    getData(url).then(data => {
        let percent = parseInt(data['info']['current'] * 100 / data['info']['total']);
        let progress_div = document.getElementById('sandbox-progress');
        progress_div.style['width'] = percent + '%';

        let status_div = document.getElementById('sandbox-config');
        let neo_sp = document.getElementById('neo-spinner')
        let p = document.createElement("p")

        if (data['state'] === 'SUCCESS') {
            progress_msg_div.innerHTML = progress_msg_div.innerHTML.replace(spinner, success)
            p.textContent = 'COMPLETE'
            progress_msg_div.innerHTML += success
            progress_msg_div.append(p)

            toastr["success"]('COMPLETE')
            let neo_port = data['info']['config']['port']
            let neo_pwd = data['info']['config']['password']

            let p1 = document.createElement('p')
            let p2 = document.createElement('p')
            p1.innerHTML = 'Port: <strong>' + neo_port + '</strong>'
            p2.innerHTML = 'Password: <strong>' + neo_pwd + '</strong>'

            status_div.appendChild(p1)
            status_div.appendChild(p2)

            // draw(neo_port, neo_pwd)
        } else if (data['state'] === 'FAILURE') {
            toastr["error"]('FAILURE')
        } else {
            if (data['state'] !== now_state) {
                if (neo_sp) {
                    progress_msg_div.innerHTML = progress_msg_div.innerHTML.replace(spinner, success)
                }

                toastr["success"](data['state'])
                if ('result' in data) {
                    p.textContent = data['result']
                } else {
                    p.textContent = data['state']
                }
                progress_msg_div.innerHTML += spinner
                progress_msg_div.append(p)
            }
            now_state = data['state']
            $(status_div.childNodes[3]).text('Result: ' + data['state']);

            // return new Promise(() => setTimeout(function () {
            //     update_progress(progress_msg_div, now_state);
            // }, 2000));
            setTimeout(function () {
                update_progress(progress_msg_div, now_state);
            }, 2000);
        }
    })
}