import {
  deleteFormData,
  getColumnsList,
  getFormDataJson,
  getTableData,
  postFormDataJson
} from "@/services/data-management/api";
import ProTable from "@ant-design/pro-table";
import type {TableListItem} from "@/pages/Admin";
import {useEffect, useState} from "react";
import JSONForm from '@/components/JSONForm'
import {Button, message, Modal, Popconfirm} from "antd";

interface propsType {
  modelName: string
}

export default ({modelName}: propsType) => {
  const [refresh, setRefresh] = useState(10086);
  const [columns, setColumns] = useState<any[]>([]);

  const optionColumn = {
    title: '操作',
    width: 180,
    key: 'option',
    valueType: 'option',
    render: (text: string, record: any) => [
      <a key="link" onClick={() => {
        Modal.info({
          title: '查看',
          content: <JSONForm model={modelName} id_={record.id} getData={getFormDataJson} isSubmitVisible={false}/>,
          width: 600,
          maskClosable: true,
          okButtonProps: {hidden: true}
        })
      }}>查看</a>,
      <a key="link2" onClick={() => {
        Modal.info({
          title: '查看',
          content: <JSONForm model={modelName} id_={record.id} getData={postFormDataJson} isSubmitVisible={true}/>,
          width: 600,
          maskClosable: true,
          okButtonProps: {hidden: true},
          closable: true,
        })
      }}>编辑</a>,
      <Popconfirm
        title="确定要删掉这条数据吗?"
        onConfirm={() => {
          deleteFormData(modelName, record.id).then(response => {
            if (response.msg === 'success') {
              message.success('删除成功')
              // setColumns(columns.filter(item => item.id !== record.id))
              setRefresh(refresh + 1)
            } else {
              message.error(`删除失败, ${response.msg}`)
            }
          })
        }}
        okText="Yes"
        cancelText="No"
      >
        <a key={'link3'}>删除</a>
      </Popconfirm>,
    ],
  }


  useEffect(() => {
    getColumnsList(modelName).then(response => {
      setColumns([...response, optionColumn])
    })
    return () => {
    };
  }, []);


  return <ProTable<TableListItem>
    key={refresh}
    columns={columns}
    request={(params, sorter, filter) => {
      // 表单搜索项会从 params 传入，传递给后端接口。
      console.log(params, sorter, filter);
      return getTableData(modelName, params).then(response => {
        return response
      })
    }}
    rowKey="key"
    pagination={{
      showQuickJumper: true,
    }}
    dateFormatter="string"
    toolbar={{
      title: '高级表格',
      tooltip: '这是一个标题提示',
    }}
    toolBarRender={() => [
      <Button
        key="3"
        type="primary"
        onClick={() => {
          Modal.info({
            title: '添加',
            content: <JSONForm model={modelName} id_={'$$9527$$'} getData={postFormDataJson} isSubmitVisible={true}/>,
            width: 600,
            maskClosable: true,
            okButtonProps: {hidden: true},
            closable: true,
            afterClose: () => {
              setRefresh(refresh + 1)
            }
          })
        }}
      >
        添加数据
      </Button>,
    ]}
  />
}
