class ViewSetPermissionByMethodMixin:
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_action_classes[self.action]]
        except KeyError:
            permission_classes = None
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get('permission_classes')

            return [permission() for permission in (permission_classes or self.permission_classes)]
