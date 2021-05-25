import {getColumnsList, getTableData} from "@/services/data-management/api";
import ProTable from "@ant-design/pro-table";
import type {TableListItem} from "@/pages/Admin";
import {useEffect, useState} from "react";
import JSONForm from '@/components/JSONForm'
import {Modal} from "antd";

interface propsType {
  modelName: string
}

export default ({modelName}: propsType) => {
  const optionColumn = {
    title: '操作',
    width: 180,
    key: 'option',
    valueType: 'option',
    render: (text: string, record: any) => [
      <a key="link" onClick={() => {
        return Modal.info({
          title: '查看',
          content: <JSONForm model={modelName} id_={record.id}/>,
          width: 600,
          maskClosable: true
        })
      }}>查看</a>,
      <a key="link2">编辑</a>,
      <a key="link3">删除</a>,
    ],
  }

  const [columns, setColumns] = useState<any[]>([]);


  useEffect(() => {
    getColumnsList(modelName).then(response => {
      setColumns([...response, optionColumn])
    })
    return () => {
    };
  }, []);


  return <ProTable<TableListItem>
    columns={columns}
    request={(params, sorter, filter) => {
      // 表单搜索项会从 params 传入，传递给后端接口。
      console.log(params, sorter, filter);
      return getTableData(modelName, params).then(response => {
        return response
      })
      // return Promise.resolve({
      //   data: tableListDataSource,
      //   success: true,
      // });
    }}
    rowKey="key"
    pagination={{
      showQuickJumper: true,
    }}
    // search={{
    //   layout: 'vertical',
    //   defaultCollapsed: false,
    // }}
    dateFormatter="string"
    toolbar={{
      title: '高级表格',
      tooltip: '这是一个标题提示',
    }}
  />
}
