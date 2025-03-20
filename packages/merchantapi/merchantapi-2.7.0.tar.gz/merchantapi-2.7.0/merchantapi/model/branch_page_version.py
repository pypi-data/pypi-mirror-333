"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

BranchPageVersion data model.
"""

from merchantapi.abstract import Model
from .version_settings import VersionSettings

class BranchPageVersion(Model):
	def __init__(self, data: dict = None):
		"""
		BranchPageVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('settings'):
			value = self.get_field('settings')
			if not isinstance(value, VersionSettings):
				self.set_field('settings', VersionSettings(value))

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_page_id(self) -> int:
		"""
		Get page_id.

		:returns: int
		"""

		return self.get_field('page_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_admin(self) -> bool:
		"""
		Get admin.

		:returns: bool
		"""

		return self.get_field('admin', False)

	def get_layout(self) -> bool:
		"""
		Get layout.

		:returns: bool
		"""

		return self.get_field('layout', False)

	def get_secure(self) -> bool:
		"""
		Get secure.

		:returns: bool
		"""

		return self.get_field('secure', False)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_title(self) -> str:
		"""
		Get title.

		:returns: string
		"""

		return self.get_field('title')

	def get_ui_id(self) -> int:
		"""
		Get ui_id.

		:returns: int
		"""

		return self.get_field('ui_id', 0)

	def get_templ_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_cache(self) -> str:
		"""
		Get cache.

		:returns: string
		"""

		return self.get_field('cache')

	def get_notes(self) -> str:
		"""
		Get notes.

		:returns: string
		"""

		return self.get_field('notes')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_source_user_id(self) -> int:
		"""
		Get source_user_id.

		:returns: int
		"""

		return self.get_field('source_user_id', 0)

	def get_source_user_name(self) -> str:
		"""
		Get source_user_name.

		:returns: string
		"""

		return self.get_field('source_user_name')

	def get_source_user_icon(self) -> str:
		"""
		Get source_user_icon.

		:returns: string
		"""

		return self.get_field('source_user_icon')

	def get_settings(self):
		"""
		Get settings.

		:returns: VersionSettings|None
		"""

		return self.get_field('settings', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'settings' in ret and isinstance(ret['settings'], VersionSettings):
			ret['settings'] = ret['settings'].to_dict()

		return ret
