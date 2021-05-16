const colors = {
    "ZZ": "#7aecec",
    "CD": "#bfeeb7",
    "BW": "#feca74",
    "LOC": "#ff9561",
    "HERB": "#aa9cfc",
    "PRESCRIPTION": "#c887fb",
    // "FACILITY": "#9cc9cc",
    // "EVENT": "#ffeb80",
    // "LAW": "#ff8197",
    // "LANGUAGE": "#ff8197",
    // "WORK_OF_ART": "#f0d0ff",
    // "DATE": "#bfe1d9",
    // "TIME": "#bfe1d9",
    // "MONEY": "#e4e7d2",
    // "QUANTITY": "#e4e7d2",
    // "ORDINAL": "#e4e7d2",
    // "CARDINAL": "#e4e7d2",
    // "PERCENT": "#e4e7d2",
}


String.prototype.format = function () {
    var formatted = this;
    for (var arg in arguments) {
        formatted = formatted.replace("{" + arg + "}", arguments[arg]);
    }
    return formatted;
};

String.prototype.strip = function () {
    return this.replace(/(^\s*)|(\s*$)/g, "");
}

String.prototype.rmspace = function () {
    return this.replace(' ', '')
};

var ent_html = '<span class="fentity"><mark class="entity" style="background: {0}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">\n' +
    '<span class="entity-label">{1}</span>' +
    '<span class="entity-text" style="font-size: 0.8em; font-weight:bold;' +
    'line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">{2}</span>\n' +
    '<button class="btn btn-link">x</button></mark></span>'


function encodeImageFileAsURL(element) {
    const file = element.files[0];
    const reader = new FileReader();
    reader.onloadend = function () {
        base64 = reader.result;
        let x = $('#show_img')[0]
        x.src = base64
        x.removeAttribute('hidden')
    }
    reader.readAsDataURL(file);
}

function prettyPrint() {
    try {
        const ugly = document.getElementById('myTextArea').value;
        const obj = JSON.parse(ugly);
        document.getElementById('myTextArea').value = JSON.stringify(obj, undefined, 4);
    } catch (e) {
        console.log('json format error', e)
    }

}

async function postData(url = '', data = {}, data_type = 'json', resp_type = 'json') {
    // Default options are marked with *
    let content_type = data_type === 'json' ? 'application/json' : 'application/x-www-form-urlencoded'
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': content_type
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    if (resp_type === 'json') {
        return response.json(); // parses JSON response into native JavaScript objects
    } else {
        return response;
    }

}

async function getData(url = '', resp_type = 'json') {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            // 'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    });
    if (resp_type === 'json') {
        return response.json(); // parses JSON response into native JavaScript objects
    } else {
        return response.text();
    }
}


function deleteData(url = '') {
    // Default options are marked with *
    const response = fetch(url, {
        method: 'Delete', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            // 'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function value_update(id) {
    let key = id.ariaLabel.replace('res-', '')
    json_res[key] = id.value;
    document.getElementById('myTextArea').value = JSON.stringify(json_res, undefined, 4);
    toastr.success(key + ' value change to ' + id.value, 'value change success')
}


function get_static_page(url, id) {
    $.ajax({
        url: url,
        type: 'get',
        contentType: false,
        processData: false,
        success: function (response) {
            const label = $('#' + id)[0];
            label.innerHTML = response
        },
    });
}

function post_pic_data() {
    if (base64) {
        const fd = new FormData();
        fd.append('img', base64)
        $.ajax({
            url: pic_url,
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response['code'] === 300) {
                    toastr.warning(response['msg'])
                } else {
                    const label = $('#pic_res')[0];
                    label.innerText = response['data']['raw_out']['ocr_result'][0]['simPred']
                    toastr.success('image data crack success', 'requests success')
                }
            },
        });
    }
}

function post_font_data() {

    const files = $('#font-file')[0].files;
    const label = $('#image-groups')[0];
    const textarea = $('#json-textarea')[0];

    label.innerHTML = '<div class="progress" style="margin-top: 100px">\n' +
        '        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="0"\n' +
        '             aria-valuemin="0" aria-valuemax="100" style="width: 0%" id="crack-progress"></div>\n' +
        '    </div>'
    textarea.setAttribute('hidden', true)

    if (files.length > 0) {
        toastr.info('start to crack font, please wait for prompting.')

        var fd = new FormData()
        fd.append('font_file', files[0])
        fd.append('type', 'html')

        const socket = io(namespace);

        socket.on('connect', function () {
            // socket.emit('my_event', {data: 'I\'m connected!'});
            // toastr.success('connect success', '', {timeOut: 500})
        });

        socket.on('my_response', function (msgs, cb) {

            if (msgs['data'].length > 0) {
                let progress = $('#crack-progress')[0];
                progress.style['width'] = msgs['width']
            }

            msgs['data'].forEach(function (msg) {
                toastr.success(msg, '', {timeOut: 1000})
            })
            if (cb)
                cb();
        });

        $.ajax({
            url: font_url,
            type: 'post',
            data: fd,
            timeout: 400 * 1000,
            contentType: false,
            processData: false,
            async: true,
            success: function (response) {
                if (response['code'] === 300) {
                    toastr.warning(response['msg'])
                } else if (response['code'] === 200) {
                    label.innerHTML = response['html'];

                    json_res = response['font_dict']
                    document.getElementById('myTextArea').value = JSON.stringify(response['font_dict'], undefined, 4);
                    textarea.removeAttribute('hidden');
                    toastr.success('font data crack success', 'requests success')
                } else {
                    toastr.error(response['msg'])
                }
            },
            error: function () {
                alert('error')
            },
            complete: function () {
                socket.emit('disconnect_request');
                socket.close()
            }
        });
    } else {
        toastr.error('没有文件是不行的')
    }
}

/**
 * 对每一块的标注结果,生成单独的card
 * 最终结果会以card组的形式进行展示
 * @param datas 后端控制返回的NER结果
 * @returns {string}
 */
function generate_cards(datas) {
    let combat_html = ''
    datas.forEach(elem => {
        texts.push(elem['text'])
        let html_tmp = generate_single_card(elem['text'], elem['ents'])
        let warp_card = '<div class="card-body annotation-card">' + html_tmp + '</div>'
        combat_html += warp_card
    })

    let head_divs = ''
    Object.entries(colors).forEach(elem => {
        let tmp_div = '<div class="btn-group"><button class="btn btn-outline-secondary tagging ' + elem[0] + '" type="button"' +
            elem[1] + '><b>' + elem[0] + '</b></button></div>'
        head_divs += tmp_div
    })
    let card_header = '<div class="card-header">' + head_divs + '</div>'

    return '<div class="card">' + card_header + combat_html + '</div>'
}

/**
 * 生成只读的card,用在历史项目查询时
 * @param datas
 * @returns {string}
 */
function generate_cards_only_read(datas) {
    let combat_html = ''
    let col_set = new Set()
    datas.forEach(elem => {
        elem['ents'].forEach(ent => {
            col_set.add(ent['label'])
        })

        let html_tmp = generate_single_card(elem['text'], elem['ents'], true)
        let warp_card = '<div class="card-body annotation-card">' + html_tmp + '</div>'
        combat_html += warp_card
    })

    let head_divs = ''
    Object.entries(colors).forEach(elem => {
        if (col_set.has(elem[0])) {
            let tmp_div = '<div class="btn-group"><p class="btn btn-outline-secondary tagging ' + elem[0] + '" type="button"' +
                elem[1] + '><b>' + elem[0] + '</b></p></div>'
            head_divs += tmp_div
        }
    })
    let card_header = '<div class="card-header">' + head_divs + '</div>'

    return '<div class="card">' + card_header + combat_html + '</div>'
}

/**
 * 生成单独的card
 * @param text
 * @param ents
 * @param only_read
 * @returns {string}
 */
function generate_single_card(text, ents, only_read = false) {
    let result = ''
    for (let i = 0; i < text.length; i++) {
        ents.forEach(elem => {
            if (i == elem['start']) {
                // let s2 = ent_html.format(colors[elem['label']],
                //     elem['label'], text.substring(elem['start'],
                //         elem['end']))
                let s2 = generate_annotation_span(text.substring(elem['start'],
                    elem['end']), elem['label'], only_read)
                result += s2.outerHTML
                i = elem['end']
            }
        })
        result += text[i]
    }
    return result
}

function tagText(tag) {
    let txt = window.getSelection(); //获取鼠标划过的对象
    var range;
    if (txt.toString().length > 0 && txt.toString().indexOf(' ') === -1) {
        let html = ent_html.format(colors[tag], tag, txt.toString())
        //txt = txt.innerHTML.substring(0, start) + html +
        // txt.innerHTML.substring(end)
        range = txt.getRangeAt(0);
        range.deleteContents();
        let span = document.createElement('span')
        range.insertNode(span);
        span.outerHTML = html;
        $(".fentity").click(function () {
            let fortext = this.innerText.strip().split(' ')
            this.outerHTML = fortext[1]
        })
    }
}


/**
 *
 * @param tag {string}
 */
function tagText1(tag) {
    let txt = window.getSelection(); //获取鼠标划过的对象
    var range;
    if (txt.toString().length > 0 && txt.toString().indexOf(' ') === -1) {
        let s1 = txt.toString()

        range = txt.getRangeAt(0);
        range.deleteContents();

        let span = generate_annotation_span(s1, tag)

        range.insertNode(span);

        $(".delete").click(function () {
            this.parentElement.outerHTML = this.parentElement.innerText.strip()
        })
    }
}

/**
 *
 * @param s1 {string}
 * @param tag {string}
 * @param only_read
 * @returns {HTMLSpanElement}
 */
function generate_annotation_span(s1, tag, only_read) {
    let span = document.createElement('span')
    span.classList.add('tag')
    span.classList.add(tag)
    span.innerText = s1;

    if (only_read) {

    } else {
        let button = document.createElement('button')
        button.classList.add('delete')
        button.classList.add('is-small')
        //button.innerText = 'x'

        span.append(button)
    }


    return span
}

function sleep(ms) {
    return new Promise(
        resolve => setTimeout(resolve, ms)
    );
}

function generate_text_and_ents_from_html(labels, contents) {
    let data_for_post = []
    let start_idx = 0
    for (let i = 0; i < texts.length; i++) {
        let tmp_data_for_post = []
        for (let j = 0; j < labels.length; j++) {
            let tmp = start_idx
            let idx = texts[i].substring(start_idx, texts[i].length)
                .indexOf(contents[j].textContent)
            start_idx = idx + contents[j].textContent.length
            tmp_data_for_post.push([idx + tmp, start_idx + tmp,
                labels[j].textContent])
        }
        data_for_post.push({
            'text': texts[i],
            'ents': tmp_data_for_post,
            'links': []   //links 暂时没有对应的处理方法
        })
    }
    return data_for_post
}

/**
 * 从（单个）card节点提取实体信息
 * @param card {Node}
 */
function generate_text_and_ents_from_html_1(card) {
    // let tags = document.getElementsByClassName('tag')
    let childs = card.childNodes;
    let ents = []
    let start_idx = 0
    childs.forEach(elem => {
        if (elem.nodeType === 1) {
            ents.push([start_idx, start_idx + elem.textContent.length, elem.classList[1]])
        } else {

        }
        start_idx += elem.textContent.length
    })
    return {
        'text': card.textContent,
        'ents': ents,
        'links': []   //links 暂时不提取
    }
}

async function update_progress(now_state = '') {
    let progress_msg_div = document.getElementById('progress-message')
    let spinner = '<div class="spinner-grow spinner-grow-sm" role="status" id="neo-spinner">' +
        '  <span class="sr-only">Loading...</span>' +
        '</div>'
    let success = '<em class="icon ni ni-list-check"></em>'
    let url = api_for_sandbox_progress.replace('none', task_id)

    await getData(url).then(data => {
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
            let p3 = document.createElement('p')
            p1.innerHTML = 'Port: <strong>' + neo_port + '</strong>'
            p2.innerHTML = 'Password: <strong>' + neo_pwd + '</strong>'
            p3.innerHTML = '<strong>请牢记</strong>'

            status_div.appendChild(p1)
            status_div.appendChild(p2)
            status_div.appendChild(p3)

            now_state = 'COMPLETE'

            // draw(neo_port, neo_pwd)
        } else if (data['state'] === 'FAILURE') {
            toastr["error"]('FAILURE')
            let p1 = document.createElement('p')
            p1.innerHTML = '创建失败'
            status_div.appendChild(p1)

            now_state = 'FAILURE'
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
        }
    })
    return now_state
}

function load_neo_page() {
    getData(page_for_neo_sanbox.replace('none', task_id)).then(data => {
        let neo_page_div = document.getElementById('neo-sandbox-page')
        neo_page_div.innerHTML = page_for_neo_sanbox
    })
}

$("#reload").click(function () {
    var cypher = $("#cypher").val();

    if (cypher.length > 3) {
        viz.renderWithCypher(cypher);
    } else {
        console.log("reload");
        viz.reload();
    }
});

async function neo_loading(data_for_post) {
    let data_tmp = ''
    let now_status1 = ''
    await postData(api_for_get_sandbox, data_for_post).then(data => {
        if (data['code'] === 200) {
            task_id = data['task_id']
            data_tmp = data
        } else {
            toastr.error(data['msg'])
        }
    })
    if (data_tmp === '') {
        return
    }

    while (true) {
        now_status1 = await update_progress(now_status1)
        if (now_status1 === 'COMPLETE') {
            break
        } else if (now_status1 === 'FAILURE') {
            break
        } else {
            await sleep(2000)
        }
    }
}

async function poll_query(query_url) {
    let now_state = 'PENDING'
    let fresh_count = 0
    while (now_state !== 'COMPLETE' && now_state !== 'FAILURE') {
        await sleep(2000).then(() => {
            getData(query_url).then(data => {
                if (data['state'] === 'COMPLETE' || data['state'] === 'SUCCESS') {
                    now_state = 'COMPLETE'
                    fresh_count = 0
                } else if (data['state'] === 'FAILURE') {
                    now_state = 'FAILURE'
                    fresh_count = 0
                } else {
                    if (now_state !== data['state']) {
                        now_state = data['state']
                        toastr.success(data['state'])
                        fresh_count = 0
                    }
                }
                if (fresh_count >= 10) {
                    now_state = 'FAILURE'
                }
                fresh_count += 1
            })
        })

    }
}

var viz;

/**
 * 知识图谱可视化
 * @param port: 图数据库端口
 * @param password: 图数据库密码
 */
function draw(port, password) {
    var config = {
        container_id: "viz",
        server_url: "bolt://localhost:" + port + '/',
        server_user: "neo4j",
        server_password: password,
        labels: {
            //"Character": "name",
            "Herb": {
                "caption": "English_name",
                "size": 1.5,
                // "sizeCypher": "MATCH (n) WHERE id(n) = {id} RETURN SIZE((n)--()) AS s;",
                "icon": "????"
            },
            "Gene": {
                "caption": "Gene_name",
                "size": 0.5,
                // "sizeCypher": "MATCH (n) WHERE id(n) = {id} RETURN SIZE((n)--()) AS s;",
                "icon": "????"
            },
            "Mol": {
                "caption": "Molecule_name",
                "size": 1.0,
                // "sizeCypher": "MATCH (n) WHERE id(n) = {id} RETURN SIZE((n)--()) AS s;",
                "icon": "????"
            },
            "TCM_symptom": {
                "caption": "TCM_symptom_name",
                "size": 0.8,
                // "sizeCypher": "MATCH (n) WHERE id(n) = {id} RETURN SIZE((n)--()) AS s;",
                "icon": "????"
            },
            // "Organization": {
            //     "caption": "name",
            //     "size": 2.0,
            //     "sizeCypher": "MATCH (n) WHERE id(n) = {id} RETURN SIZE((n)--()) AS s",
            //     "icon": "???"
            // }

        },
        relationships: {
            // "PRESIDENT": {
            //     "caption": "El Presidente"
            // }
        },
        // initial_cypher: "match (p:Person)-[r]-(o:Organization)-[r1]-(p2:Person) RETURN * LIMIT 10",
        initial_cypher: "MATCH (n:Herb) RETURN n LIMIT 25",
        arrows: false
    };

    viz = new NeoVis.default(config);
    viz.render();
    console.log(viz);

}

/**
 * 非结构化数据-第一步-excel类型-点击事件处理
 */
function normal_excel_click_handler(event) {
    // 处理文本数据中,excel数据的点击事件
    let file = document.getElementById("csv-file").files[0];
    let formData = new FormData();
    formData.append("file", file);
    fetch(api_for_my_model_file, {
        method: "POST",
        body: formData
    }).then(data => {
        return data.json()
    }).then(data => {
        if (data['code'] === 200) {
            let textfiled = document.getElementById('show-res');

            textfiled.innerHTML = generate_cards(data['data'])

            annotation_handler()

            wizard_changer(event, 3, 5, $('#myTab a[href="#placementPanel"]'))
        } else {
            toastr.error(data['msg'])
        }
    });
}

/**
 * 非结构化数据-第一步-文本类型-点击事件处理
 * @param event
 */
function text_data_click_handler(event) {
    let data4post = {'message': document.getElementById('data4post').value}
    postData(api_for_my_model, data4post).then(data => {
        if (data['code'] === 200) {
            let textfiled = document.getElementById('show-res');

            textfiled.innerHTML = generate_cards(data['data'])

            annotation_handler()

            wizard_changer(event, 3, 5, $('#myTab a[href="#placementPanel"]'))

        } else {
            toastr.error(data['msg'])
        }
    });
}

/**
 * 非结构化数据-第一步-文件类型-点击事件处理
 * @param event
 */
function text_file_click_handler(event) {
    let file = document.getElementById("text-file").files[0];
    let formData = new FormData();
    formData.append("file", file);
    fetch(api_for_my_model_file, {
        method: "POST",
        body: formData
    }).then(data => {
        return data.json()
    }).then(data => {
        if (data['code'] === 200) {
            let textfiled = document.getElementById('show-res');

            textfiled.innerHTML = generate_cards(data['data'])

            annotation_handler()

            wizard_changer(event, 3, 5, $('#myTab a[href="#placementPanel"]'))
        } else {
            toastr.error(data['msg'])
        }
    });

}

/**
 * 非结构化数据, 假模型的事件处理
 * @param event
 */
function text_file_to_fake_model_click_handler(event) {
    let data4post = {'message': document.getElementById('data4post').value}
    postData(api_for_fake_model, data4post).then(data => {
        let textfiled = document.getElementById('show-res');
        textfiled.innerHTML = generate_cards(data['data'])
    }).then(_ => {
        annotation_handler()

        wizard_changer(event, 3, 5, $('#myTab a[href="#placementPanel"]'))
    })

}

/**
 * 非结构化数据-第三步-构建neo4j的sandbox
 * @param event
 * @returns {Promise<void>}
 */
async function text_file_to_build_neo4j_sandbox(event) {
    let name_div = document.getElementById('new-project-name');
    let description_div = document.getElementById('new-project-description');
    if (name_div.value === "") {
        toastr.warning('project name can`t be empty')
        return
    }

    wizard_changer(event, 4, 5, $('#myTab a[href="#schedulePanel"]').tab('show'))

    let annotation_cards = document.getElementsByClassName('annotation-card')

    let data_list_for_post = []
    for (let i = 0; i < annotation_cards.length; i++) {
        data_list_for_post.push(generate_text_and_ents_from_html_1(annotation_cards[i]))
    }

    let need_email = document.getElementById('need-email')

    let data_for_post = {
        'data_list': data_list_for_post,
        'project_name': name_div.value,
        'need_email': need_email.checked,
        'description': description_div.value
    }

    await neo_loading(data_for_post)

    sleep(2000).then(() => {
        wizard_changer(event, 5, 5, $('#myTab a[href="#reviewPanel"]').tab('show'))
    })
}

/**
 * 结构化数据-第一步-解析表格-事件处理
 * @param event
 */
function KE_from_DB_click_handler(event) {
    let db_config_form = document.getElementById('form-data-of-database-config')
    let db_config = new FormData(db_config_form)
    let data = {}
    for (let pair of db_config.entries()) {
        data[pair[0]] = pair[1]
    }
    postData(api_for_knowledge_extract_from_db, data).then(data => {
        if (data['code'] === 200) {
            let textfiled = document.getElementById('show-res');
            let innerHtml = ''
            data['tables'].forEach(item => {
                innerHtml += generate_knowledge_datatable_card(item)
            })
            textfiled.innerHTML = innerHtml

            wizard_changer(event, 3, 5, $('#myTab a[href="#placementPanel"]'))
        } else {
            toastr.error(data['msg'])
        }
    });
}

/**
 * 从json中提取数据
 * @param event
 */
function extract_knowledge_from_json_file_click_handler(event) {
    let files = document.getElementById("json-file").files;
    let formData = new FormData();
    // formData.append('file', files);
    files.forEach(item => {
        formData.append(item['name'], item);
    })


    fetch(api_for_knowledge_extract_from_json_file, {
        method: "POST",
        body: formData
    }).then(data => {
        return data.json()
    }).then(data => {
        if (data['code'] === 200) {
            alert('success')
        } else {
            toastr.error(data['msg'])
        }
    })
}

/**
 * 生成单个的表格卡片
 * @param table  html string
 */
function generate_knowledge_datatable_card(table) {
    return `<div class="card"><div class="card-inner"><h5 class="card-title">${table['table_name']}</h5><p class="card-text">${table['html']}</p></div></div>`
}

// function generate_knowledge_datatable_title() {
//
// }

/**
 * 监听标注事件
 */
function annotation_handler() {
    $(".delete").click(function () {
        this.parentElement.outerHTML = this.parentElement.innerText.strip()
    })

    $(".tagging").click(function () {
        tagText1(this.innerText);
    })
}

/**
 * 变更wizard-progress组件的状态
 * @param event 点击事件
 * @param pre_step_number 当前的进度
 * @param total_step_number 总共进度长度
 * @param tab_selector
 */
function wizard_changer(event, pre_step_number, total_step_number, tab_selector) {
    document.getElementById('step' + pre_step_number).classList.remove('disabled')
    event.preventDefault();
    let progress = document.getElementById('global-progress');
    progress.style['width'] = pre_step_number / total_step_number * 100 + '%';
    progress.innerText = `Step ${pre_step_number} of ${total_step_number}`;
    tab_selector.tab('show');
}