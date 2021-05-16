import ProList from '@ant-design/pro-list';

export interface runtimeDataProp {
  title: string;
  subTitle: string | JSX.Element;
  type: string;
  avatar: string;
  content: string | JSX.Element;
  actions: any[] | JSX.Element;
  status: string;
}

export default ({
  runtimeData,
  headerTitle,
}: {
  runtimeData: runtimeDataProp[];
  headerTitle: string;
}) => {
  return (
    <ProList<any>
      headerTitle={headerTitle}
      pagination={{
        defaultPageSize: 6,
        showSizeChanger: false,
      }}
      grid={{ gutter: 16, column: 3 }}
      showActions="hover"
      metas={{
        title: {
          search: false,
        },
        subTitle: {
          search: false,
        },
        type: {
          search: false,
        },
        avatar: {
          search: false,
        },
        content: {
          search: false,
        },
        actions: {
          search: false,
        },
      }}
      dataSource={runtimeData}
    />
  );
};
