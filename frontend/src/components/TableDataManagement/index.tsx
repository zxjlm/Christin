import {getColumnsList, getTableData} from "@/services/data-management/api";
import ProTable from "@ant-design/pro-table";
import type {TableListItem} from "@/pages/Admin";
import {useEffect, useState} from "react";

const optionColumn = {
  title: '操作',
  width: 180,
  key: 'option',
  valueType: 'option',
  render: (text: string, record: string, _: any, action: any) => [
    <a key="link" onClick={() => {
      console.log(text, record, action)
    }}>查看</a>,
    <a key="link2">编辑</a>,
    <a key="link3">删除</a>,
  ],
}

export default ({modelName}: { modelName: string }) => {
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
