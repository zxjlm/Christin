export default [
  {
    path: '/user',
    layout: false,
    routes: [
      {
        path: '/user',
        routes: [
          {
            name: 'login',
            path: '/user/login',
            component: './user/Login',
          },
        ],
      },
    ],
  },
  {
    path: '/graphinneo',
    layout: false,
    routes: [
      {
        path: '/graphinneo',
        routes: [
          {
            name: 'graph',
            path: '/graphinneo/graph/:port/:pwd',
            component: './AntNeo/index',
          },
        ],
      },
    ],
  },
  {
    path: '/welcome',
    name: 'welcome',
    icon: 'smile',
    component: './Welcome',
  },
  {
    path: '/project-management',
    name: 'project-management',
    icon: 'smile',
    component: './ProjectsManagement/index',
  },
  {
    path: '/create-project',
    name: 'create-project',
    icon: 'smile',
    component: './CreateProject/index',
  },
  {
    path: '/admin',
    name: 'admin',
    icon: 'crown',
    access: 'canAdmin',
    component: './Admin',
    routes: [
      {
        path: '/admin/sub-page',
        name: 'sub-page',
        icon: 'smile',
        component: './Welcome',
      },
    ],
  },
  {
    name: 'list.table-list',
    icon: 'table',
    path: '/list',
    component: './TableList',
  },
  {
    path: '/',
    redirect: '/welcome',
  },
  {
    component: './404',
  },
];
