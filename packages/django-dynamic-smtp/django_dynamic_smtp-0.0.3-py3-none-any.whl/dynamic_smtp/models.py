from typing import override

from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from tinymce.models import HTMLField


class AbstractEmailConfiguration(SingletonModel):
    activated = models.BooleanField(
        default=False,
        verbose_name=_("Email está ativado?"),
        help_text=_(
            "Só ative essa opção depois de testar as configurações de "
            + "email no botão ao lado. Quando ativado, as notificações vão "
            + "ser enviadas por email e será possível a usuários "
            + "redefinir suas senhas."
        ),
    )
    host = models.CharField(
        max_length=128,
        verbose_name=_("Host"),
        default="smtp.gmail.com",
    )
    port = models.PositiveIntegerField(
        verbose_name=_("Porta"),
        default=587,
    )
    username = models.CharField(
        max_length=128,
        verbose_name=_("Usuário"),
        default="example@gmail.com",
    )
    password = models.CharField(
        max_length=128,
        verbose_name=_("Senha"),
        default="1234",
    )
    use_tls = models.BooleanField(
        default=True,
        verbose_name=_("Usar TLS"),
    )
    use_ssl = models.BooleanField(
        default=False,
        verbose_name=_("Usar SSL"),
    )
    timeout = models.IntegerField(
        blank=True,
        null=True,
        default=120,
        verbose_name=_("Timeout"),
    )
    from_name = models.CharField(
        max_length=255,
        verbose_name=_("Nome do remetente"),
        null=True,
        blank=True,
    )
    from_email = models.EmailField(
        verbose_name=_("Email remetente"),
        default="admin@example.com",
    )
    signature = HTMLField(
        blank=True,
        null=True,
        verbose_name=_("Assinatura dos emails"),
        help_text=format_html(
            "{}<code>{}</code>{}",
            _("Para usar essa assinatura em seus emails, utilize a variável "),
            "{{ signature }}",
            ".",
        ),
    )

    @override
    def __str__(self):
        return str(self._meta.verbose_name)

    class Meta:
        verbose_name = _("Email configuration")
        abstract = True


class EmailConfiguration(AbstractEmailConfiguration):
    pass
